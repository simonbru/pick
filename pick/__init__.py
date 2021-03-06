#-*-coding:utf-8-*-

# import curses
from .screen_win import Screen

__all__ = ['Picker', 'pick']


KEYS_ENTER = (ord('\r'), ord('\n'), ord('\r'))
KEYS_UP = (b'\xe0H', ord('k'),)
KEYS_DOWN = (b'\xe0P', ord('j'),)
KEYS_SELECT = (b'\xe0M', ord(' '),)

class Picker(object):
    """The :class:`Picker <Picker>` object

    :param options: a list of options to choose from
    :param title: (optional) a title above options list
    :param multi_select: (optional) if true its possible to select multiple values by hitting SPACE, defaults to False
    :param indicator: (optional) custom the selection indicator
    :param default_index: (optional) set this if the default selected option is not the first one
    """

    def __init__(self, options, title=None, indicator='*', default_index=0, multi_select=False, min_selection_count=0):

        if len(options) == 0:
            raise ValueError('options should not be an empty list')

        self.options = options
        self.title = title
        self.indicator = indicator
        self.multi_select = multi_select
        self.min_selection_count = min_selection_count
        self.all_selected = []

        if default_index >= len(options):
            raise ValueError('default_index should be less than the length of options')

        if multi_select and min_selection_count > len(options):
            raise ValueError('min_selection_count is bigger than the available options, you will not be able to make any selection')

        self.index = default_index
        self.custom_handlers = {}

        self.screen = Screen()

    def register_custom_handler(self, key, func):
        self.custom_handlers[key] = func

    def move_up(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.options) - 1

    def move_down(self):
        self.index += 1
        if self.index >= len(self.options):
            self.index = 0

    def mark_index(self):
        if self.multi_select:
            if self.index in self.all_selected:
                self.all_selected.remove(self.index)
            else:
                self.all_selected.append(self.index)

    def get_selected(self):
        """return the current selected option as a tuple: (option, index)
           or as a list of tuples (in case multi_select==True)
        """
        if self.multi_select:
            return_tuples = []
            for selected in self.all_selected:
                return_tuples.append((self.options[selected], selected))
            return return_tuples
        else:
            return self.options[self.index], self.index

    def get_title_lines(self):
        if self.title:
            return [*self.title.split('\n'), '']
        return []

    def get_option_lines(self):
        lines = []
        for index, option in enumerate(self.options):
            if index == self.index:
                prefix = self.indicator
            else:
                prefix = len(self.indicator) * ' '

            if self.multi_select and index in self.all_selected:
                # format = curses.color_pair(1)
                # TODO format
                format = None
                line = ('{0} {1}'.format(prefix, option), format)
            else:
                line = '{0} {1}'.format(prefix, option)
            lines.append(line)

        return lines

    def get_lines(self):
        title_lines = self.get_title_lines()
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def draw(self):
        """draw the curses ui on the screen, handle scroll if needed"""

        # Add one line of margin
        self.screen.add_line('')
        max_rows = self.screen.rows - 1

        lines, current_line = self.get_lines()

        # calculate how many lines we should scroll, relative to the top
        scroll_top = getattr(self, 'scroll_top', 0)
        if current_line <= scroll_top:
            scroll_top = 0
        elif current_line - scroll_top > max_rows:
            scroll_top = current_line - max_rows
        self.scroll_top = scroll_top

        lines_to_draw = lines[scroll_top:scroll_top + max_rows]

        for line in lines_to_draw:
            self.screen.add_line(' ' + line)
        self.screen.refresh()

    def run_loop(self):
        while True:
            self.draw()
            c = self.screen.getch()
            if c in KEYS_UP:
                self.move_up()
            elif c in KEYS_DOWN:
                self.move_down()
            elif c in KEYS_ENTER:
                if self.multi_select and len(self.all_selected) < self.min_selection_count:
                    continue
                return self.get_selected()
            elif c in KEYS_SELECT and self.multi_select:
                self.mark_index()
            elif c in self.custom_handlers:
                ret = self.custom_handlers[c](self)
                if ret:
                    return ret

    def start(self):
        # TODO: something
        result = self.run_loop()
        print()
        return result


def pick(options, title=None, indicator='*', default_index=0, multi_select=False, min_selection_count=0):
    """Construct and start a :class:`Picker <Picker>`.

    Usage::

      >>> from pick import pick
      >>> title = 'Please choose an option: '
      >>> options = ['option1', 'option2', 'option3']
      >>> option, index = pick(options, title)
    """
    picker = Picker(options, title, indicator, default_index, multi_select, min_selection_count)
    return picker.start()
