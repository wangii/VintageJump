import sublime
import sublime_plugin

LAST_SELECTION_KEY = 'last_selection'


class VintagJumpEventListener(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        s = view.sel()[0]
        print "s: %d, %d" % (s.a, s.b)
        if s.b == s.a:
            return

        last_selection = view.settings().get(LAST_SELECTION_KEY, {})
        last_selection[str(view.id())] = {'a': s.a, 'b': s.b}
        view.settings().set(LAST_SELECTION_KEY, last_selection)

    # def on_modified(self, view):
    #     s = view.sel()[0]
    #     print "selection: %d, %d" % (s.a, s.b)
    #     print view.settings().get('command_mode')

        # def on_key_change(self):
        #     pass


class ReselectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        last_selection = self.view.settings().get(LAST_SELECTION_KEY, {})
        sel = last_selection.get(str(self.view.id()), None)

        if sel is None:
            return

        self.view.sel().clear()
        reg = sublime.Region(long(sel['a']), long(sel['b']))
        self.view.sel().add(reg)
        self.view.show_at_center(reg)
