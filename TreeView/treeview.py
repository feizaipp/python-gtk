#! /usr/bin/python
#coding=utf-8

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Pango, Gdk

sbox_info = [("test", "root", "test-1556098225", "2019-4-24 17:30", 0),
                        ("test1", "root", "test1-1556106806", "2019-4-24 19:53", 0),
                        ("test2", "root", "test2-1556106816", "2019-4-24 19:53", 0),
                        ("测试", "root", "test2-1556106816", "2019-3-24 19:53", 1),
                        ("2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222", "root", "test2-1556106816", "2019-3-24 19:53", 1)]

UI_INFO = """
<ui>
  <popup name='PopupMenu'>
    <menuitem action='Test' />
  </popup>
  <popup name='PopupTitleMenu'>
    <menuitem action='Name' />
    <menuitem action='Dircetory' />
    <menuitem action='Time' />
    <menuitem action='Status' />
  </popup>
</ui>
"""


class TreeViewFilterWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Treeview Filter Demo")
        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.create_model()
        tv = Gtk.TreeView(model=self.model)
        tv.set_rules_hint(True)
        tv.set_search_column(1)
        tv.columns_autosize ()
        #tv.set_headers_clickable(False)
        tv.connect("button-press-event", self.on_button_press_event)
        self.grid.add(tv)
        self.add_columns(tv)

        self.treeview = tv

        action_group = Gtk.ActionGroup("my_actions")
        self.add_popup_actions(action_group)
        self.add_popup_title_actions(action_group)
        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)
        self.popup = uimanager.get_widget("/PopupMenu")
        self.popuptitle = uimanager.get_widget("/PopupTitleMenu")
    
    def add_popup_actions(self, action_group):
        action_group.add_actions([
            ("Test", None, "test", None, None,
            self.test_press)])

    def add_popup_title_actions(self, action_group):
        name = Gtk.ToggleAction("Name", "名称", None, None)
        name.set_active(True)
        name.set_sensitive(False)
        name.connect("toggled", self.on_title_choices_toggled)
        action_group.add_action(name)

        dircetory = Gtk.ToggleAction("Dircetory", "目录", None, None)
        dircetory.connect("toggled", self.on_title_choices_toggled)
        action_group.add_action(dircetory)

        mtime = Gtk.ToggleAction("Time", "修改时间", None, None)
        mtime.set_active(True)
        mtime.connect("toggled", self.on_title_choices_toggled)
        action_group.add_action(mtime)

        status = Gtk.ToggleAction("Status", "状态", None, None)
        status.set_active(True)
        status.set_sensitive(False)
        status.connect("toggled", self.on_title_choices_toggled)
        action_group.add_action(status)

    def get_column_title(self, name):
        if name == "Name":
            return "名称"
        elif name == "Dircetory":
            return "目录"
        elif name == "Time":
            return "修改时间"
        elif name == "Status":
            return "状态"

    def on_title_choices_toggled(self, widget):
        columns = self.treeview.get_columns()
        for column in columns:
            if column.get_title() == self.get_column_title(widget.get_name()):
                if widget.get_active():
                    column.set_visible(True)
                else:
                    column.set_visible(False)

    def test_press(self, widget):
        select = self.treeview.get_selection()
        model, treeiter = select.get_selected()
        if treeiter != None:
            print("You selected %s")  % model[treeiter][1]

    def create_ui_manager(self):
        uimanager = Gtk.UIManager()

        # Throws exception if something went wrong
        uimanager.add_ui_from_string(UI_INFO)

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager

    def create_model(self):
        self.model = Gtk.ListStore(bool,
                                   str,
                                   str,
                                   str,
                                   str)
        for info in sbox_info:
            status = "关闭"
            if info[4] == 0:
                status = "关闭"
            else:
                status = "打开"
            self.model.append([False, info[0], info[2], info[3], status])
        
    def add_columns(self, treeview):
        model = treeview.get_model()
        renderer = Gtk.CellRendererToggle()
        renderer.connect('toggled', self.is_fixed_toggled, model)
        column = Gtk.TreeViewColumn("选项", renderer, active=0)
        column.set_fixed_width(50)
        column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        treeview.append_column(column)

        renderer = Gtk.CellRendererText(ellipsize=Pango.EllipsizeMode.END,
                                         ellipsize_set=True)
        column = Gtk.TreeViewColumn("名称", renderer, text=1)
        column.set_sort_column_id(1)
        column.set_resizable(True)
        column.set_expand(True)
        column.get_button().connect("button-press-event", self.on_column_header_button_press_event)
        treeview.append_column(column)

        renderer = Gtk.CellRendererText(ellipsize=Pango.EllipsizeMode.END,
                                         ellipsize_set=True)
        column = Gtk.TreeViewColumn("目录", renderer, text=2)
        column.set_sort_column_id(2)
        column.set_resizable(True)
        column.set_expand(True)
        column.get_button().connect("button-press-event", self.on_column_header_button_press_event)
        treeview.append_column(column)
        column.set_visible(False)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("修改时间", renderer, text=3)
        column.set_sort_column_id(3)
        column.set_resizable(True)
        column.set_expand(True)
        column.get_button().connect("button-press-event", self.on_column_header_button_press_event)
        treeview.append_column(column)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("状态", renderer, text=4)
        column.set_sort_column_id(4)
        column.set_resizable(True)
        column.set_expand(True)
        column.get_button().connect("button-press-event", self.on_column_header_button_press_event)
        treeview.append_column(column)

    def on_column_header_button_press_event(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            self.popuptitle.popup(None, None, None, None, event.button, event.time)

    def on_button_press_event(self, treeview, event):
        if treeview and event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            if treeview.get_path_at_pos(int(event.x), int(event.y)) == None:
                return
            #select = self.treeview.get_selection()
            #model, treeiter = select.get_selected()
            if event.window == treeview.get_bin_window():
                self.popup.popup(None, None, None, None, event.button, event.time)

    def is_fixed_toggled(self, cell, path_str, model):
        # get toggled iter
        iter_ = model.get_iter(path_str)
        is_fixed = model.get_value(iter_, 0)

        # do something with value
        is_fixed ^= 1

        model.set_value(iter_, 0, is_fixed)


def print_tree_store(store):
    rootiter = store.get_iter_first()
    print_rows(store, rootiter, "")

def print_rows(store, treeiter, indent):
    while treeiter is not None:
        print(indent + str(store[treeiter][:]))
        if store.iter_has_child(treeiter):
            childiter = store.iter_children(treeiter)
            print_rows(store, childiter, indent + "\t")
        treeiter = store.iter_next(treeiter)

win = TreeViewFilterWindow()

win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()