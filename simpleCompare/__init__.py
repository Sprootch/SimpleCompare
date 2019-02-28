from fman import DirectoryPaneCommand, show_alert, load_json, OK, CANCEL, DirectoryPane
from fman.url import as_human_readable
import subprocess
from .settings import Settings

# TODO it would be good to display it in the "CompareWithSaved" command in the command palete
"""Currently selcted file to compare"""
savedToCompare = ""
settings = Settings()

class SaveToCompare(DirectoryPaneCommand):
    def __call__(self):
        global savedToCompare
        savedToCompare = self.get_chosen_files()[0]

    def is_visible(self):
        files = self.get_chosen_files()
        return len(files) == 1


class CompareWithSaved(DirectoryPaneCommand):
    def __call__(self):
        global savedToCompare
        selectedFile = self.get_chosen_files()[0]
        ComparisonToolRunner.compare_files(savedToCompare, selectedFile)
        pass

    def is_visible(self):
        global savedToCompare
        return savedToCompare != "" and len(self.get_chosen_files()) == 1

class CompareFiles(DirectoryPaneCommand):
    def __call__(self):
        selectedFile1 = self.get_chosen_files()[0]
        selectedFile2 = self.get_chosen_files()[1]
        ComparisonToolRunner.compare_files(selectedFile1, selectedFile2)
        pass

    def is_visible(self):
        return len(self.get_chosen_files()) == 2

class CompareSelectedFiles(DirectoryPaneCommand):
    def __call__(self):
        selectedFile1 = self.pane.window.get_panes()[0].get_selected_files()[0]
        selectedFile2 = self.pane.window.get_panes()[1].get_selected_files()[0]
        ComparisonToolRunner.compare_files(selectedFile1, selectedFile2)
        pass

    def is_visible(self):
        leftPane = self.pane.window.get_panes()[0]
        rightPane = self.pane.window.get_panes()[1]
        return len(leftPane.get_selected_files()) == 1 and len(rightPane.get_selected_files()) == 1

class ComparisonToolRunner:
    @staticmethod
    def compare_files(lhsFile: str, rhsFile: str):
        global settings
        comparisonTool = settings.get_comparison_tool()
        if comparisonTool:
            subprocess.call([comparisonTool, as_human_readable(lhsFile), as_human_readable(rhsFile)])

def _ifnull(var, val):
  if var is None:
    return val
  return var
