# Source material:
# W3School Python Syntax
# Provided documents
# Documentation about Datetime library

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)


class Notebook:

    def __init__(self):
        try:
            self.tree = ET.parse("notes.xml")
        except FileNotFoundError:
            self.tree = ET.ElementTree(ET.Element("data"))
        self.root = self.tree.getroot()

    def add_note(self, topic, note, text, timestamp):
        topic_elements = self.root.findall(f".//topic[@name='{topic}']")
        if not topic_elements:
            topic_element = ET.SubElement(
                self.root, "topic", {"name": topic})
        else:
            topic_element = topic_elements[0]

        note_element = ET.SubElement(topic_element, "note", {"name": note})
        text_element = ET.SubElement(note_element, "text")
        text_element.text = text
        timestamp_element = ET.SubElement(note_element, "timestamp")
        timestamp_element.text = timestamp

        ET.dump(self.tree)
        self.tree.write("notes.xml")
        return "Note added!"

    def get_notes(self, topic):
        topic_element = self.root.find(f".//topic[@name='{topic}']")
        if topic_element is None:
            return "No notes found!"

        notes = []
        for note_element in topic_element.findall("note"):
            text_element = note_element.find("text")
            timestamp_element = note_element.find("timestamp")
            notes.append({"name": note_element.get(
                "name"), "text": text_element.text, "timestamp": timestamp_element.text})

        return notes


with SimpleXMLRPCServer(("localhost", 3000), requestHandler=RequestHandler) as server:
    server.register_instance(Notebook())
    print("Server started")
    server.serve_forever()
