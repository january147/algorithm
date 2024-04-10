xml_string="""<?xml version="1.0"?>
<collection shelf="New Arrivals">
<movie title="Enemy Behind">
   <type>War, Thriller</type>
   <format>DVD</format>
   <year>2003</year>
   <rating>PG</rating>
   <stars>10</stars>
   <description>Talk about a US-Japan war</description>
</movie>
<movie title="Transformers">
   <type>Anime, Science Fiction</type>
   <format>DVD</format>
   <year>1989</year>
   <rating>R</rating>
   <stars>8</stars>
   <description>A schientific fiction</description>
</movie>
<movie title="Trigun">
   <type>Anime, Action</type>
   <format>DVD</format>
   <episodes>4</episodes>
   <rating>PG</rating>
   <stars>10</stars>
   <description>Vash the Stampede!</description>
</movie>
<movie title="Ishtar">
   <type>Comedy</type>
   <format>VHS</format>
   <rating>PG</rating>
   <stars>2</stars>
   <description>Viewable boredom</description>
</movie>
</collection>
"""

import xml.etree.ElementTree as ET
import json


tree = ET.fromstring(xml_string)
result = tree.findall('.//*[@title="Ishtar"]')
print(result)

def search_nodes_by_xpath(xml_file, xpath):
    """
    Search nodes in xml file using xpath.

    :param xml_file: A string of xml file path.
    :param xpath: A string of xpath.
    :return: A list of nodes.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return root.findall(xpath)


def json_to_xml(json_str):
    """
    Convert json string to xml string.

    :param json_str: A json string.
    :return: An xml string.
    """
    try:
        json_dict = json.loads(json_str)
    except json.JSONDecodeError:
        return json_str
    tag = json_dict.get("type", "collection")
    attrs = {attr: json_dict.get(attr) for attr in json_dict if attr not in {"type", "children"}}
    inner_xml = ''.join(_json_to_xml_node(child)
                       for child in json_dict.get("children", []))
    xml_str = "<{tag} {attrs}>{inner_xml}</{tag}>".format(tag=tag, attrs=" ".join('{}="{}"'.format(key, val) for key, val in attrs.items()), inner_xml=inner_xml)
    return xml_str


def _json_to_xml_node(node_dict):
    if isinstance(node_dict, str):
        return "<{tag}>{value}</{tag}>".format(tag=node_dict.get("type", "node"), value=node_dict)
    tag = node_dict.get("type", "node")
    attrs = {attr: node_dict.get(attr) for attr in node_dict if attr not in {"type", "children"}}
    if "value" in node_dict:
        xml_str = "<{tag} {attrs}>{value}</{tag}>".format(tag=tag, attrs=" ".join('{}="{}"'.format(key, val) for key, val in attrs.items()), value=node_dict["value"])
    else:
        inner_xml = ''.join(_json_to_xml_node(child)
                            for child in node_dict.get("children", []))
        xml_str = "<{tag} {attrs}>{inner_xml}</{tag}>".format(tag=tag, attrs=" ".join('{}="{}"'.format(key, val) for key, val in attrs.items()), inner_xml=inner_xml)
    return xml_str




sample_json = """
{
    "type": "Animals",
    "version": "1.0",
    "date": "2019-07-07",
    "author": "Jianfeng Wu",
    "children": [
        {
            "type": "Mammals",
            "classification": "Mammalia",
            "children": [
                {
                    "type": "Monkeys",
                    "endemism": "Africa",
                    "children": [
                        {"type": "Chimpanzee", "name": "Chimp", "population": "20,000", "habitat": "West and Central Africa"},
                        {"type": "Orangutan", "name": "Orang", "population": "10,000", "habitat": "Indonesia"}
                    ]
                },
                {
                    "type": "Cats",
                    "classification": "Felidae",
                    "children": [
                        {"type": "Lion", "name": "Lion", "population": "25,000", "habitat": "Africa"},
                        {"type": "Tiger", "name": "Tiger", "population": "30,000", "habitat": "Asia"}
                    ]
                }
            ]
        },
        {
            "type": "Birds",
            "classification": "Aves",
            "children": [
                {"type": "Eagle", "name": "Eagle", "population": "100,000", "habitat": "Nearly every continent"},
                {"type": "Owl", "name": "Owl", "population": "50,000", "habitat": "Every continent"}
            ]
        },
        {
            "type": "Reptiles",
            "classification": "Reptilia",
            "children": [
                {
                    "type": "Snakes",
                    "children": [
                        {
                            "type": "Viper",
                            "children": [
                                {"type": "Cobra", "name": "Cobra", "population": "20,000", "habitat": "Sub-Saharan Africa"},
                                {"type": "Rattlesnake", "name": "Rattlesnake", "population": "10,000", "habitat": "North America"}
                            ]
                        },
                        {
                            "type": "Boas",
                            "children": [
                                {"type": "AfricanBoa", "name": "AfricanBoa", "population": "5,000", "habitat": "West and Central Africa"},
                                {"type": "BallPython", "name": "BallPython", "population": "15,000", "habitat": "Worldwide"}
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}
"""



from xml.dom.minidom import parseString

xml_str = json_to_xml(sample_json)
print(xml_str)
xml = parseString(xml_str)
formatted_xml_str = xml.toprettyxml(indent="    ")
print(formatted_xml_str)



sample_json_list = json.loads(sample_json)
sample_json_list["children"][0]["children"][0]["children"] += sample_json_list["children"][0]["children"][0]["children"] * 9999
sample_json = json.dumps(sample_json_list)

size_in_KB = len(sample_json) / 1024
print("Size of sample_json: {:.2f}KB".format(size_in_KB))

with open("sample_json.json", "w") as f:
    f.write(sample_json)




def json_to_xml_speed_test(json_str):
    import time
    print("Start json_to_xml speed test...")
    start = time.time()
    for i in range(1000):
        xml_str = json_to_xml(json_str)
        if i % 100 == 0:
            print("progress: {}%".format(i/10))
    end = time.time()
    cost = (end - start)/1000
    print("json_to_xml cost: {}s".format(cost))
    print("json_to_xml speed: {}ops".format(1/cost))


# json_to_xml_speed_test(sample_json)



# import xml.etree.ElementTree as ET

# parse xml
xml_str = json_to_xml(sample_json)
root = ET.fromstring(xml_str)

# find a node with attribute name="Cobra" using xpath
node = root.find(".//*[@name='Cobra']")

# print the node
print(ET.tostring(node).decode())

