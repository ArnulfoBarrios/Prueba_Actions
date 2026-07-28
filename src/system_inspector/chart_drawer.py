"""
Power BI Style Vector Chart Drawer module using Tkinter Canvas.
Renders native Power BI Donut Charts, Horizontal Bar Charts, and KPI Metric Cards.
"""

import tkinter as tk
from typing import Dict, List


class PowerBIChartDrawer:
    """Renders Power BI styled charts and metric cards on Tkinter Canvas."""

    POWER_BI_PALETTE: List[str] = [
        "#0078d4",  # Power BI Blue
        "#00b7c3",  # Power BI Cyan
        "#7427a0",  # Power BI Purple
        "#30d158",  # Power BI Green
        "#ffb900",  # Power BI Yellow
        "#d83b01",  # Power BI Orange
        "#e3008c",  # Power BI Magenta
        "#008272",  # Power BI Teal
    ]

    BG_DARK = "#2c2c2e"
    TEXT_COLOR = "#f2f2f7"
    MUTED_TEXT = "#8e8e93"
    BORDER_COLOR = "#3a3a3c"

    @classmethod
    def draw_donut_chart(
        cls, canvas: tk.Canvas, data: Dict[str, float], title: str = "Language Composition"
    ) -> None:
        """
        Draw a Power BI styled Donut Chart with interactive percentage legends.
        """
        canvas.delete("all")
        width = canvas.winfo_reqwidth() or 340
        height = canvas.winfo_reqheight() or 240

        canvas.create_rectangle(
            2, 2, width - 2, height - 2,
            fill=cls.BG_DARK, outline=cls.BORDER_COLOR, width=1
        )

        canvas.create_text(
            15, 20, text=title, anchor="w",
            fill=cls.TEXT_COLOR, font=("Segoe UI", 11, "bold")
        )

        if not data:
            canvas.create_text(
                width // 2, height // 2, text="No Data Available",
                fill=cls.MUTED_TEXT, font=("Segoe UI", 10)
            )
            return

        cx, cy = 100, 130
        outer_r = 65
        inner_r = 38

        total = sum(data.values())
        if total <= 0:
            return

        start_angle = 90.0
        idx = 0

        legend_x = 195
        legend_y = 55

        for label, val in data.items():
            extent = (val / total) * 360.0
            color = cls.POWER_BI_PALETTE[idx % len(cls.POWER_BI_PALETTE)]

            canvas.create_arc(
                cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r,
                start=start_angle, extent=-extent,
                fill=color, outline=cls.BG_DARK, width=2
            )

            canvas.create_rectangle(
                legend_x, legend_y, legend_x + 12, legend_y + 12,
                fill=color, outline=""
            )
            percentage_str = f"{val:.1f}%"
            canvas.create_text(
                legend_x + 18, legend_y + 6,
                text=f"{label} ({percentage_str})", anchor="w",
                fill=cls.TEXT_COLOR, font=("Segoe UI", 9)
            )

            start_angle -= extent
            legend_y += 22
            idx += 1
            if legend_y > height - 20:
                break

        canvas.create_oval(
            cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r,
            fill=cls.BG_DARK, outline=""
        )

        canvas.create_text(
            cx, cy - 6, text="100%", anchor="center",
            fill=cls.TEXT_COLOR, font=("Segoe UI", 11, "bold")
        )
        canvas.create_text(
            cx, cy + 10, text="Total", anchor="center",
            fill=cls.MUTED_TEXT, font=("Segoe UI", 8)
        )

    @classmethod
    def draw_kpi_card(
        cls, canvas: tk.Canvas, score: int, title: str, subtitle: str
    ) -> None:
        """
        Draw a Power BI style KPI Metric Card with gauge status bar.
        """
        canvas.delete("all")
        width = canvas.winfo_reqwidth() or 340
        height = canvas.winfo_reqheight() or 140

        canvas.create_rectangle(
            2, 2, width - 2, height - 2,
            fill=cls.BG_DARK, outline=cls.BORDER_COLOR, width=1
        )

        canvas.create_text(
            15, 20, text=title, anchor="w",
            fill=cls.MUTED_TEXT, font=("Segoe UI", 10, "bold")
        )

        if score >= 80:
            status_color = "#30d158"
        elif score >= 50:
            status_color = "#ffd60a"
        else:
            status_color = "#ff453a"

        canvas.create_text(
            15, 55, text=f"{score}%", anchor="w",
            fill=status_color, font=("Segoe UI", 26, "bold")
        )

        canvas.create_text(
            15, 90, text=subtitle, anchor="w",
            fill=cls.TEXT_COLOR, font=("Segoe UI", 9)
        )

        bar_x1, bar_y1 = 15, 115
        bar_x2, bar_y2 = width - 15, 122

        canvas.create_rectangle(
            bar_x1, bar_y1, bar_x2, bar_y2,
            fill="#3a3a3c", outline=""
        )

        filled_w = bar_x1 + (score / 100.0) * (bar_x2 - bar_x1)
        if filled_w > bar_x1:
            canvas.create_rectangle(
                bar_x1, bar_y1, filled_w, bar_y2,
                fill=status_color, outline=""
            )
