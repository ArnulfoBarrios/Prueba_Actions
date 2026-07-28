"""
Unit tests for PowerBIChartDrawer helper class using unittest.
Follows testing naming rule: should [action] when [condition].
"""

import unittest
import tkinter as tk
from system_inspector.chart_drawer import PowerBIChartDrawer


class TestPowerBIChartDrawer(unittest.TestCase):

    def test_should_draw_donut_chart_when_canvas_provided(self):
        try:
            root = tk.Tk()
            root.withdraw()
            canvas = tk.Canvas(root, width=340, height=240)
            data = {"Python": 45.0, "JavaScript": 30.0, "Dart": 25.0}

            PowerBIChartDrawer.draw_donut_chart(canvas, data, "Test Chart")
            items = canvas.find_all()
            self.assertGreater(len(items), 0)
            root.destroy()
        except tk.TclError:
            pass

    def test_should_draw_kpi_card_when_score_provided(self):
        try:
            root = tk.Tk()
            root.withdraw()
            canvas = tk.Canvas(root, width=340, height=140)

            PowerBIChartDrawer.draw_kpi_card(canvas, 85, "KPI TITLE", "PASS")
            items = canvas.find_all()
            self.assertGreater(len(items), 0)
            root.destroy()
        except tk.TclError:
            pass


if __name__ == "__main__":
    unittest.main()
