# Note: this is somewhat hackish and needs to be integrated into the main
# latin-conjugations.pv file at some point

import re
import yaml

directory = "/Users/harukaeru/Workspace/latin-conjugations/"


with open(directory + "latin-conjugations-worksheet.yaml", "r") as f:
    data = yaml.full_load(f.read())

page_width = 792
page_height = 612

heading_size = 7
group_heading_size = 7
word_size = 9
horizontal_spacing = 63
default_spacing = 13 # line spacing
group_header_size = 9
group_header_offset = 16
row_spacing = 130

size(page_width, page_height)
background(1)

font("YuMincho", size=11)

stylesheet("ending", weight="bold")

def style_line(l):
    # swap out [ending] for <ending>ending</ending>
    text_line = re.sub(r"\{(.*?)\}", r"<stem>\1</stem>", l)
    text_line = re.sub(r"\[(.*?)\]", r"<ending>\1</ending>", text_line)
    return "<w>%s</w>" % text_line

def draw_chart(x, y, chart, fill_color="#cb202c", spacing=default_spacing):
    push()
    translate(x, y)

    font("YuMincho", size=word_size, tracking=-8)
    fill(0)

    stylesheet("ending", fill=fill_color, weight="bold")

    pen(0.5)
    stroke(0.5)
    for l in chart:
        if l != '':
            line(0, 1, 50, 1)

        # line spacing
        translate(0, spacing)

    font(tracking=0)

    pop()

def draw_group(x, y, group, fill_color="#cb202c", spacing=default_spacing):
    push()
    translate(x, y)

    if group['chart']:
        font("PT Sans", size=group_heading_size, tracking=15)
        fill(0.5)
        if group['title']:
            text(group['title'].upper(), 0, 0)
        font(tracking=0)

        draw_chart(0, group_header_offset, group['chart'], fill_color, spacing)

    pop()

def draw_headings(x, y, headings, spacing=default_spacing):
    push()
    translate(x, y + group_header_offset - 0.75)
    font("YuMincho", size=heading_size, sc=True)
    fill(0.5)

    for line in headings:
        text(line, 0, 0)

        # line spacing
        translate(0, spacing)

    font(sc=False)
    pop()

def draw_group_header(x, y, label, width):
    push()
    fill(0)
    stroke(0.5)
    translate(x, y)
    font("PT Sans", size=group_header_size, tracking=15)
    line(0, -11, width, -11)
    text(label.upper(), 0, 0)
    font(tracking=0)
    pop()

def parse_list(groups):
    response = []

    for line in groups:
        data = line.split('|')

        group = {
            'title': data[0].strip(),
            'chart': [x.strip() for x in data[1:]],
        }

        response.append(group)

    return response

headings = [
    '1st sg.',
    '2nd sg.',
    '3rd sg.',
    '1st pl.',
    '2nd pl.',
    '3rd pl.',
]

active_headings = [
    'active',
    'passive',
]

gerund_headings = [
    'gen.',
    'dat.',
    'acc.',
    'abl.',
]

margin = 30

# Heading

font("PT Sans", size=14, tracking=15)
text("Latin — Conjugation Worksheet".upper(), margin, margin + 10)

align(RIGHT)
font("YuMincho", size=9, italic=True, tracking=0)
stroke(0)
fill(0.5)
text("bencrowder.net — Last modified 1 November 2018", page_width-margin, margin + 10)
font(italic=False)

align(LEFT)
text("Word: ", margin, margin + 25)

pen(0.5)

# Groups

base_y = margin + 50

for group in data['left']:
    draw_group_header(margin, base_y, group['title'], 430)
    draw_headings(30, base_y + 20, headings)

    for index, g in enumerate(parse_list(group['groups'])):
        draw_group(margin + 40 + (index * horizontal_spacing), base_y + 20, g, fill_color=group['fill'])

    base_y += row_spacing

# Right side
right_x = 520
base_y = margin + 50

for group in data['right']:
    if 'type' in group and group['type'] == 'headerless':
        headings_list = gerund_headings
        base = base_y + 4
    else:
        headings_list = active_headings
        base = base_y + 20

    draw_group_header(right_x, base_y, group['title'], 242)
    draw_headings(right_x, base, headings_list)

    for index, g in enumerate(parse_list(group['groups'])):
        draw_group(right_x + 40 + (index * horizontal_spacing), base, g, fill_color=group['fill'])

    base_y += row_spacing

if 'note' in data:
    font("YuMincho", size=8, italic=True, tracking=0)
    text(data['note'], right_x, page_height - margin - 11)


export(directory + "latin-conjugations-worksheet.pdf")
