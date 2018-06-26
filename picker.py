#!/usr/bin/python

# This code is available for use under CC0 (Creative Commons 0 - universal). 
# You can copy, modify, distribute and perform the work, even for commercial
# purposes, all without asking permission. For more information, see LICENSE.md or 
# https://creativecommons.org/publicdomain/zero/1.0/

# usage:
# opts = Picker(
#    title = 'Delete all files',
#    options = ["Yes", "No"]
# ).getSelected()

# returns a simple list
# cancel returns False

import curses

class Picker:
    """Allows you to select from a list with curses"""
    stdscr = None
    win = None
    title = ""
    arrow = ""
    footer = ""
    more = ""
    c_selected = ""
    c_empty = ""
    
    cursor = 0
    offset = 0
    selected = 0
    selcount = 0
    aborted = False
    
    window_padding = 2
    window_height = 0
    window_width = 0
    entry_height = 0
    all_options = []
    length = 0
    
    win = False
    
    def curses_start(self):
        self.stdscr = curses.initscr()
        self.stdscr.keypad(1)
        curses.noecho()
        curses.cbreak()
        self.resize_window()
        self.win = curses.newwin(
            self.window_height - self.window_padding * 2,
            self.window_width - self.window_padding * 2,
            self.window_padding,
            self.window_padding
        )
    
    def resize_window(self):
        self.window_height, self.window_width = self.stdscr.getmaxyx()
        if self.win != False:
            self.entry_height = self.window_height - self.window_padding * 2
            self.win.resize(
                self.window_height - self.window_padding * 2,
                self.window_width - self.window_padding * 2,
            )
            self.win.clear()
            self.redraw()
            curses.doupdate()
    
    def curses_stop(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def getSelected(self):
        if self.aborted == True:
            return( False )

        ret_s = filter(lambda x: x["selected"], self.all_options)
        ret = map(lambda x: x["label"], ret_s)
        return( ret )

    def text(self, y, x, label):
        try:
            self.win.addstr(y, x, label)
        
        except:
            pass
        
    def redraw(self):
        self.win.clear()
        self.win.border(
            self.border[0], self.border[1],
            self.border[2], self.border[3],
            self.border[4], self.border[5],
            self.border[6], self.border[7]
        )
        
        # user instructions
        self.text(
            self.window_height - ((self.window_padding*2)+1),
            5,
            " " + self.footer + " "
        )
        
        position = 0
        range = self.all_options[self.offset:self.offset+self.entry_height-4]
        for option in range:
            if option["selected"] == True:
                line_label = self.c_selected + " "
            else:
                line_label = self.c_empty + " "
            
            #self.win.addstr(position + 2, 5, line_label + option["label"])
            self.text(position+2, 5, line_label + option["label"])
            position = position + 1
            
        # hint for more content above
        if self.offset > 0:
            self.text(1, 5, self.more)
        
        # hint for more content below
        if self.offset + self.window_height <= self.length - 2:
            self.text(self.entry_height-2, 5, self.more)
        
        self.text(0, 5, " " + self.title + " ")
        self.text(
            0, self.window_width - ((self.window_padding*2) + 9),
            " " + str(self.selcount) + "/" + str(self.length) + " "
        )
        self.text(self.cursor + 2,1, self.arrow)
        self.win.refresh()

    def check_cursor_up(self):
        # scroll up
        if self.cursor < 0:
            self.cursor = 0
            if self.offset > 0:
                self.offset -= 1
    
    def check_cursor_down(self):
        # reached bottom of window, scroll down
        if self.cursor >= self.entry_height-5:
            self.cursor = self.entry_height-5
            self.offset += 1

        # window not filled all the way with entries
        if self.cursor > self.length - 1:
            self.cursor = self.length - 1

        # reached bottom of window and list, stop
        if self.offset + self.cursor >= self.length:
            self.offset = self.offset - 1
    
    def check_page_up(self):
        if self.offset < 0:
            self.offset = 0
            self.cursor = 0

    def check_page_down(self):
        if self.offset + self.entry_height-4 > self.length:
            self.offset = self.length - self.entry_height+4
            self.cursor = self.entry_height-5
            
            if self.offset < 0:
                self.offset = 0
            
        if self.cursor > self.length - 1:
            self.cursor = self.length - 1
    
    def mostly_checked(self):
        count_checked = 0;
        count_unchecked = 0;
        
        for option in self.all_options:
            if option["selected"] == True:
                count_checked += 1
            else:
                count_unchecked += 1

        if count_checked >= count_unchecked:
            return True
        else:
            return False
        
    def curses_loop(self, stdscr):
        while 1:
            resize = curses.is_term_resized(self.window_width, self.window_height)
            if resize == True:
                self.resize_window()
                
            self.redraw()
            c = stdscr.getch()
            
            if c == ord('q') or c == ord('Q'):
                self.aborted = True
                break
            elif c == ord('a') or c == ord('A'):
                set_to = self.mostly_checked()
                for option in self.all_options:
                    option["selected"] = not set_to
            elif c == curses.KEY_UP:
                self.cursor = self.cursor - 1
                self.check_cursor_up()
            elif c == curses.KEY_DOWN:
                self.cursor = self.cursor + 1
                self.check_cursor_down()
            elif c == curses.KEY_PPAGE:
                self.offset -= self.entry_height
                self.check_page_up()
            elif c == curses.KEY_NPAGE:
                self.offset += self.entry_height
                self.check_page_down()
            elif c == ord(' '):
                self.all_options[self.selected]["selected"] = \
                    not self.all_options[self.selected]["selected"]
            elif c == 10:
                break

            # compute selected position only after dealing with limits
            self.selected = self.cursor + self.offset
            
            temp = self.getSelected()
            self.selcount = len(temp)
    
    def __init__(
        self, 
        options, 
        title='Select', 
        arrow="-->",
        footer="Space = toggle, Enter = accept, q = cancel, a = all",
        more="...",
        border="||--++++",
        c_selected="[X]",
        c_empty="[ ]"
    ):
        self.title = title
        self.arrow = arrow
        self.footer = footer
        self.more = more
        self.border = border
        self.c_selected = c_selected
        self.c_empty = c_empty
        
        self.all_options = []
        
        for option in options:
            self.all_options.append({
                "label": option,
                "selected": False
            })
            self.length = len(self.all_options)
        
        self.curses_start()
        curses.wrapper( self.curses_loop )
        self.curses_stop()
