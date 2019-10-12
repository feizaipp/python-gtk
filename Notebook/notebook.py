#! /usr/bin/python
#coding=utf-8

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Pango, Gdk
import os

notebook = None

def on_next_clicked(self, *args):
    notebook.next_page()
    pass

def on_prev_clicked(self, *args):
    notebook.prev_page()
    pass

win = Gtk.Window()
win.connect("destroy", Gtk.main_quit)

overlay = Gtk.Overlay()

table = Gtk.Table()
overlay.add_overlay(table)
win.add(overlay)

notebook = Gtk.Notebook()
notebook.set_tab_pos(Gtk.PositionType.BOTTOM)

table.attach_defaults(notebook, 0, 6, 0, 1)

left_revealer = Gtk.Revealer()
left_revealer.set_transition_duration(1000)
left_revealer.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
left_revealer.set_halign(Gtk.Align.START)
left_revealer.set_valign(Gtk.Align.CENTER)
left_revealer.set_margin_start(12)
left_revealer.set_margin_end(12)
overlay.add_overlay(left_revealer)

right_revealer = Gtk.Revealer()
right_revealer.set_transition_duration(1000)
right_revealer.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
right_revealer.set_halign(Gtk.Align.END)
right_revealer.set_valign(Gtk.Align.CENTER)
right_revealer.set_margin_start(12)
right_revealer.set_margin_end(12)
overlay.add_overlay(right_revealer)

button = Gtk.Button("next")
#button.new_from_icon_name("go-next-symbolic", Gtk.IconSize.BUTTON)
button.connect("clicked", on_next_clicked)
right_revealer.add(button)

button = Gtk.Button("prev")
#button.new_from_icon_name("go-previous-symbolic", Gtk.IconSize.BUTTON)
button.connect("clicked", on_prev_clicked)
left_revealer.add(button)

right_revealer.set_reveal_child(True)
left_revealer.set_reveal_child(True)



'''
for i in xrange(5):
    text = "Notebook %d" % i
    frame = Gtk.Frame()
    label = Gtk.Label(text)
    frame.add(label)

    label = Gtk.Label(text)
    notebook.append_page(frame, None)
'''
lists = os.listdir("/home/xxx/work/test/python/ui/img")
for l in lists:
    img = Gtk.Image.new_from_file(os.path.join("/home/xxx/work/test/python/ui/img", l))
    img.show()
    notebook.append_page(img, None)

notebook.set_scrollable(True)
notebook.set_show_tabs(False)



win.show_all()
Gtk.main()


