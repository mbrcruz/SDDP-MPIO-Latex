from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
FIGURES_DIR = ROOT / "figuras"


PATHS = {
    "sd_current": ROOT / "Pesquisas" / "Results" / "SDumont" / "Lustre - 1536 Series - Sem rede" / "plot.csv",
    "sd_mpiio": ROOT / "Pesquisas" / "Results" / "SDumont" / "Lustre - 1536 Series - Sem rede - MPIO" / "plot.csv",
    "aws_current": ROOT / "Pesquisas" / "Results" / "AWS" / "Lustre - 1536 Series - Sem rede" / "plot.csv",
    "aws_mpiio": ROOT / "Pesquisas" / "Results" / "AWS" / "Lustre - 1536 Series - Sem rede- MPIO" / "plot.csv",
}


COLORS = {
    "current": "#4C78A8",
    "mpiio": "#F58518",
    "io": "#54A24B",
    "comm": "#E45756",
    "collective": "#72B7B2",
    "sim": "#9D755D",
    "size_1": "#4C78A8",
    "size_2": "#72B7B2",
    "size_3": "#F58518",
    "size_4": "#E45756",
}


def read_csv(path: Path, max_nodes: int | None = None) -> pd.DataFrame:
    df = pd.read_csv(path)
    if max_nodes is not None:
        df = df[df["Nodes"] <= max_nodes]
    return df.sort_values("Nodes")


def finish(fig: plt.Figure, output: str) -> None:
    fig.tight_layout()
    FIGURES_DIR.mkdir(exist_ok=True)
    fig.savefig(FIGURES_DIR / output, dpi=300, bbox_inches="tight")
    plt.close(fig)


def bandwidth_plot(current: pd.DataFrame, mpiio: pd.DataFrame, output: str) -> None:
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    ax.errorbar(
        current["Nodes"],
        current["Avg_bandwidth"],
        yerr=current["Stddev_bandwidth"],
        marker="o",
        linewidth=2,
        capsize=4,
        color=COLORS["current"],
        label="Atual",
    )
    ax.errorbar(
        mpiio["Nodes"],
        mpiio["Avg_bandwidth"],
        yerr=mpiio["Stddev_bandwidth"],
        marker="s",
        linewidth=2,
        capsize=4,
        color=COLORS["mpiio"],
        label="MPI-IO",
    )
    ax.set_xlabel("Nós")
    ax.set_ylabel("Banda agregada média (Gb/s)")
    ax.set_xticks(sorted(set(current["Nodes"]).union(set(mpiio["Nodes"]))))
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend(frameon=False)
    finish(fig, output)


def time_plot(current: pd.DataFrame, mpiio: pd.DataFrame, output: str) -> None:
    nodes = current["Nodes"].to_numpy()
    x = np.arange(len(nodes))
    width = 0.38

    fig, ax = plt.subplots(figsize=(10.5, 6.2))

    def stacked(df: pd.DataFrame, xpos: np.ndarray, label_suffix: str) -> None:
        sim = df["Avg_Simulation"].to_numpy()
        io = df["Avg_io_per_process"].to_numpy()
        comm = df["Avg_comunication_per_process"].to_numpy()
        collective_col = (
            "Avg_mpiCollective_per_process"
            if "Avg_mpiCollective_per_process" in df.columns
            else "Avg_mpiopen_per_process"
        )
        collective = df.get(collective_col, pd.Series(np.zeros(len(df)))).to_numpy()

        ax.bar(xpos, sim, width, color=COLORS["sim"], label=f"Simulação {label_suffix}")
        ax.bar(xpos, io, width, bottom=sim, color=COLORS["io"], label=f"I/O {label_suffix}")
        ax.bar(xpos, comm, width, bottom=sim + io, color=COLORS["comm"], label=f"Comunicação {label_suffix}")
        ax.bar(
            xpos,
            collective,
            width,
            bottom=sim + io + comm,
            color=COLORS["collective"],
            label=f"Coletivas {label_suffix}",
        )

    stacked(current, x - width / 2, "Atual")
    stacked(mpiio, x + width / 2, "MPI-IO")

    ax.set_xlabel("Nós")
    ax.set_ylabel("Tempo médio por processo (s)")
    ax.set_xticks(x)
    ax.set_xticklabels(nodes)
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend(ncols=2, frameon=False, fontsize=8)
    finish(fig, output)


def message_size_plot(current: pd.DataFrame, mpiio: pd.DataFrame, output: str) -> None:
    classes = ["pequenas", "médias", "grandes", "muito grandes"]
    cols = [f"Avg_time_per_record{i}" for i in range(1, 5)]
    cur_vals = current[cols].mean().to_numpy()
    mpi_vals = mpiio[cols].mean().to_numpy()

    x = np.arange(len(classes))
    width = 0.38
    fig, ax = plt.subplots(figsize=(10.2, 4.8))
    ax.bar(x - width / 2, cur_vals, width, color=COLORS["current"], label="Atual")
    ax.bar(x + width / 2, mpi_vals, width, color=COLORS["mpiio"], label="MPI-IO")
    ax.set_yscale("log")
    ax.set_xlabel("Classe de tamanho da mensagem")
    ax.set_ylabel("Tempo médio de bloqueio (s)")
    ax.set_xticks(x)
    ax.set_xticklabels(classes)
    ax.grid(True, axis="y", which="both", alpha=0.3)
    ax.legend(frameon=False)
    finish(fig, output)


def message_count_by_size_plot(output: str) -> None:
    log_dir = (
        ROOT
        / "Pesquisas"
        / "Results"
        / "AWS"
        / "Lustre - 1536 Series - Sem rede"
        / "2-nodes"
        / "1"
    )
    sizes = []
    for path in sorted(log_dir.glob("mpiio-*.log")):
        with path.open(errors="ignore") as log_file:
            for line in log_file:
                fields = line.strip().split(",")
                if len(fields) < 8:
                    continue
                try:
                    sizes.append(int(float(fields[-1])))
                except ValueError:
                    continue

    bins = [
        ("Ate 1 KB", 0, 1024),
        ("1 KB a 64 KB", 1024, 64 * 1024),
        ("64 KB a 1 MB", 64 * 1024, 1024 * 1024),
        ("Acima de 1 MB", 1024 * 1024, float("inf")),
    ]
    counts = []
    for _, lower, upper in bins:
        counts.append(sum(1 for size in sizes if lower <= size < upper))

    total = sum(counts)
    percentages = [count / total * 100 if total else 0 for count in counts]
    labels = [label for label, _, _ in bins]
    colors = [COLORS[f"size_{i}"] for i in range(1, 5)]
    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(10.5, 4.9))
    bars = ax.barh(y, counts, color=colors, height=0.62)
    ax.set_xscale("log")
    ax.set_xlabel("Quantidade de mensagens (escala logaritmica)")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.grid(True, axis="x", which="both", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar, count, percentage in zip(bars, counts, percentages):
        ax.text(
            count * 1.08,
            bar.get_y() + bar.get_height() / 2,
            f"{count:,} ({percentage:.1f}%)".replace(",", "."),
            va="center",
            fontsize=10,
        )

    ax.set_xlim(1, max(counts) * 2.2)
    finish(fig, output)


def result_file_format_plot(output: str) -> None:
    fig, ax = plt.subplots(figsize=(12.6, 5.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    colors = {
        "meta": "#E8F1FA",
        "meta_border": "#2B6CB0",
        "values": "#EAF6EA",
        "values_border": "#2F855A",
        "row": "#F7FBFF",
        "text": "#263238",
        "muted": "#607D8B",
        "highlight": "#FFF3CD",
        "highlight_border": "#B7791F",
        "offset": "#D97706",
    }

    def box(x, y, w, h, face, edge, lw=1.5):
        rect = plt.Rectangle((x, y), w, h, facecolor=face, edgecolor=edge, linewidth=lw)
        ax.add_patch(rect)
        return rect

    def text(x, y, label, size=10, weight="normal", color=None, ha="center", va="center"):
        ax.text(x, y, label, fontsize=size, fontweight=weight, color=color or colors["text"], ha=ha, va=va)

    table_x, table_y = 1.45, 1.2
    row_h = 0.58
    col_widths = [1.08, 1.08, 1.08, 1.34, 1.34, 1.34, 0.74, 1.34]
    headers = [
        "Estágios",
        "Cenários",
        "Hora",
        "Elemento 1",
        "Elemento 2",
        "Elemento 3",
        "...",
        "Elemento N",
    ]
    rows = [
        ["1", "1", "1", "142.37", "88.04", "317.92", "...", "51.68"],
        ["1", "1", "2", "139.85", "91.27", "305.44", "...", "49.13"],
        ["...", "...", "...", "...", "...", "...", "...", "..."],
        ["2", "1", "1", "156.20", "74.66", "288.09", "...", "63.41"],
        ["...", "...", "...", "...", "...", "...", "...", "..."],
        ["E", "S", "H", "121.09", "96.58", "334.71", "...", "57.24"],
    ]

    x = table_x
    for idx, (header, width) in enumerate(zip(headers, col_widths)):
        is_meta = idx < 3
        face = colors["meta"] if is_meta else colors["values"]
        edge = colors["meta_border"] if is_meta else colors["values_border"]
        box(x, table_y + row_h * len(rows), width, row_h, face, edge, lw=1.8)
        text(x + width / 2, table_y + row_h * len(rows) + row_h / 2, header, 8.9, "bold", edge)
        x += width

    for row_idx, row in enumerate(rows):
        y = table_y + row_h * (len(rows) - 1 - row_idx)
        x = table_x
        for col_idx, (value, width) in enumerate(zip(row, col_widths)):
            is_meta = col_idx < 3
            face = "#FFFFFF" if row_idx % 2 == 0 else colors["row"]
            edge = "#B8C2CC"
            if row_idx == len(rows) - 1:
                face = colors["highlight"] if is_meta else "#F8FFF8"
                edge = colors["highlight_border"] if is_meta else "#B8C2CC"
            box(x, y, width, row_h, face, edge, lw=1.0)
            text(x + width / 2, y + row_h / 2, value, 7.4 if col_idx >= 3 else 8.8, color=colors["text"])
            x += width

    stage_offsets = [
        (0, "offset\nestágio 1"),
        (3, "offset\nestágio 2"),
        (5, "offset\nestágio E"),
    ]
    for row_idx, label in stage_offsets:
        y = table_y + row_h * (len(rows) - 1 - row_idx) + row_h / 2
        text(table_x - 0.42, y, label, 7.5, "bold", colors["offset"], ha="right")
        ax.annotate(
            "",
            xy=(table_x - 0.02, y),
            xytext=(table_x - 0.32, y),
            arrowprops=dict(arrowstyle="-|>", color=colors["offset"], linewidth=1.3),
        )

    meta_w = sum(col_widths[:3])
    values_x = table_x + meta_w
    values_w = sum(col_widths[3:])
    text(table_x + meta_w / 2, 0.65, "Colunas de identificação do registro", 9.4, "bold", colors["meta_border"])
    text(values_x + values_w / 2, 0.65, "Valores gravados a partir da coluna 4", 9.4, "bold", colors["values_border"])

    ax.annotate(
        "",
        xy=(table_x + meta_w / 2, table_y - 0.03),
        xytext=(table_x + meta_w / 2, 0.85),
        arrowprops=dict(arrowstyle="-|>", color=colors["meta_border"], linewidth=1.4),
    )
    ax.annotate(
        "",
        xy=(values_x + values_w / 2, table_y - 0.03),
        xytext=(values_x + values_w / 2, 0.85),
        arrowprops=dict(arrowstyle="-|>", color=colors["values_border"], linewidth=1.4),
    )

    finish(fig, output)


def sddp_timeline_plot(output: str) -> None:
    fig, ax = plt.subplots(figsize=(12.4, 5.6))
    ax.set_xlim(-0.25, 10.8)
    ax.set_ylim(-0.2, 4.65)
    ax.axis("off")

    colors = {
        "resolve": "#54A24B",
        "io": "#e57373",
        "coord": "#F2C94C",
        "comm": "#4C78A8",
        "line": "#D8DEE9",
        "text": "#263238",
        "muted": "#607D8B",
    }

    processes = [
        ("Rank 0\nProcesso Distribuidor", 3.3, 0.18, 0.72, []),
        ("Rank 1", 2.35, 0.45, 0.28, [(2, 2.05), (6, 0.7), (10, 2.2)]),
        ("Rank 2", 1.4, 0.45, 0.44, [(3, 1.55), (7, 0.62), (11, 1.15), (12, 0.72)]),
        ("Rank N", 0.45, 0.45, 0.84, [(4, 0.9), (8, 2.8), ("X", 1.1)]),
    ]
    coord_start_x = 0.15
    final_coord_end_x = 9.00
    file_open_width = 0.32
    open_end_x = (
        max(coord_start_x + initial_comm_width + tasks[0][1] for _, _, initial_comm_width, _, tasks in processes[1:])
        + file_open_width
    )
    io_widths = [0.34, 0.38, 0.36, 0.30]
    post_io_comm_widths = [
        [0.35, 0.35, 0.35],
        [0.35, 0.35, 0.35],
        [0.35, 0.35, 0.35, 0.35],
        [0.35, 0.35, 0.35],
    ]

    def block(x, y, w, h, color, label, edge="white", hatch=None, size=10):
        rect = plt.Rectangle(
            (x, y - h / 2),
            w,
            h,
            facecolor=color,
            edgecolor=edge,
            linewidth=1.3,
            hatch=hatch,
            zorder=3,
        )
        ax.add_patch(rect)
        ax.text(
            x + w / 2,
            y,
            label,
            ha="center",
            va="center",
            fontsize=size,
            color="white",
            weight="bold",
            zorder=4,
        )

    for process_index, (process, y, initial_comm_width, final_comm_width, tasks) in enumerate(processes):
        ax.hlines(y, 0.0, 9.75, color=colors["line"], linewidth=2.0, zorder=1)
        ax.text(-0.08, y, process, ha="right", va="center", fontsize=10.5, color=colors["text"], weight="bold")
        if process_index == 0:
            coordinator_end_x = final_coord_end_x + processes[-1][3]
            block(coord_start_x, y, coordinator_end_x - coord_start_x, 0.3, colors["comm"], "", size=8.5)
            continue
        x = coord_start_x
        block(x, y, initial_comm_width, 0.3, colors["comm"], f"{tasks[0][0]}", size=8.0)
        x += initial_comm_width
        for idx, (scenario, compute_width) in enumerate(tasks):
            label_size = 6.0 if compute_width < 0.8 else 7.2 if compute_width < 1.1 else 8.8
            block(x, y, compute_width, 0.5, colors["resolve"], f"{scenario}", size=label_size)
            x += compute_width
            if idx == 0:
                block(x, y, open_end_x - x, 0.5, colors["coord"], "", size=8.5)
                x = open_end_x
            block(x, y, io_widths[idx], 0.34, colors["io"], f"{scenario}", size=8.0)
            x += io_widths[idx]
            is_last = idx == len(tasks) - 1
            if not is_last:
                next_scenario = tasks[idx + 1][0]
                block(x, y, post_io_comm_widths[process_index][idx], 0.3, colors["comm"], f"{next_scenario}", size=8.0)
                x += post_io_comm_widths[process_index][idx]
        block(x, y, final_coord_end_x - x, 0.5, colors["coord"], "", size=8.5)
        x = final_coord_end_x
        block(x, y, final_comm_width, 0.3, colors["comm"], "Fim", size=8.0)

    legend_y = 4.28
    legend_items = [
        (0.95, colors["resolve"], "Computação resolvendo cenário X"),
        (4.55, colors["io"], "E/S"),
        (5.65, colors["comm"], "Comunicação"),
        (7.25, colors["coord"], "MPI_File_open/MPI_File_close"),
    ]
    for x, color, label in legend_items:
        ax.add_patch(plt.Rectangle((x, legend_y - 0.13), 0.28, 0.26, facecolor=color, edgecolor="none"))
        ax.text(x + 0.38, legend_y, label, ha="left", va="center", fontsize=10.4, color=colors["text"])

    finish(fig, output)


def sddp_architecture2_plot(output: str) -> None:
    fig, ax = plt.subplots(figsize=(12.8, 7.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.45)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    colors = {
        "process": "#EAF2FB",
        "process_border": "#2B6CB0",
        "compute": "#54A24B",
        "io": "#e57373",
        "shared": "#F7FBFF",
        "shared_border": "#2B6CB0",
        "lustre": "#E9F7EF",
        "lustre_border": "#2E7D32",
        "stripe_a": "#BFE6C5",
        "stripe_b": "#7BC67E",
        "text": "#263238",
        "muted": "#607D8B",
        "arrow": "#2E7D32",
        "note": "#FFF7E6",
        "note_border": "#B7791F",
        "dash": "#B0B0B0",
    }
    process_colors = {
        "P1": "#2B6CB0",
        "P2": "#D97706",
        "PN-1": "#7C3AED",
        "PN": "#C53030",
    }

    def box(x, y, w, h, face, edge, lw=1.6, radius=0.06):
        patch = plt.Rectangle((x, y), w, h, facecolor=face, edgecolor=edge, linewidth=lw)
        ax.add_patch(patch)
        return patch

    def text(x, y, s, size=10, weight="normal", color=None, ha="center", va="center", style="normal"):
        ax.text(x, y, s, fontsize=size, fontweight=weight, color=color or colors["text"], ha=ha, va=va, style=style)

    def arrow(x1, y1, x2, y2, color=None, lw=1.5, alpha=1.0):
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(arrowstyle="-|>", color=color or colors["arrow"], linewidth=lw, alpha=alpha, shrinkA=0, shrinkB=0),
        )

    def curved_arrow(x1, y1, x2, y2, rad=0.0, color=None, lw=1.5, alpha=1.0):
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>",
                color=color or colors["arrow"],
                linewidth=lw,
                alpha=alpha,
                shrinkA=0,
                shrinkB=0,
                connectionstyle=f"arc3,rad={rad}",
            ),
        )

    process_specs = [
        (0.55, 5.85, "P1", "Rank 0\nProcesso Distribuidor", "distribui tarefas"),
        (3.1, 5.85, "P2", "Rank 1", "cenários 2, 6, 10"),
        (5.55, 5.85, None, "...", ""),
        (7.3, 5.85, "PN-1", "Rank N-1", "cenários 3, 7, 11"),
        (9.85, 5.85, "PN", "Rank N", "cenários 4, 8, X"),
    ]
    process_centers = {}
    for x, y, key, title, subtitle in process_specs:
        if title == "...":
            box(x, y, 1.15, 0.95, "#F7F7F7", colors["dash"], lw=1.2)
            text(x + 0.58, y + 0.47, "...", 20, "bold", colors["muted"])
            continue
        process_color = process_colors[key]
        box(x, y, 1.75, 1.05, colors["process"], process_color, lw=2.0)
        box(x, y + 0.94, 1.75, 0.11, process_color, process_color, lw=0.0)
        text(x + 0.88, y + 0.75, title, 9.2 if "\n" in title else 11, "bold", process_color)
        text(x + 0.88, y + 0.38, subtitle, 8.8, color=colors["muted"])
        process_centers[key] = (x + 0.88, y)

    shared_x, shared_y, shared_w, shared_h = 0.6, 3.55, 10.8, 1.75
    box(shared_x, shared_y, shared_w, shared_h, colors["shared"], colors["shared_border"])
    text(shared_x + shared_w / 2, shared_y + shared_h - 0.25, "Arquivos Compartilhados", 14, "bold", colors["process_border"])

    file_y = 3.70
    file_count = 8
    file_gap = 0.18
    file_w = 0.96
    file_h = 0.86
    file_x0 = shared_x + (shared_w - file_count * file_w - (file_count - 1) * file_gap) / 2
    file_specs = [
        ("Arquivo1", []),
        ("Arquivo2", [("P2", 0.90), ("PN-1", 0.80)]),
        ("Arquivo3", []),
        ("Arquivo4", [("PN", 0.70)]),
        ("Arquivo5", [("P2", 0.60)]),
        ("Arquivo6", [("PN-1", 0.50), ("PN", 0.40)]),
        ("Arquivo7", [("P2", 0.30)]),
        ("ArquivoN", [("PN-1", 0.20), ("PN", 0.10)]),
    ]
    file_colors = [
        "#B3E2CD",
        "#FDCDAC",
        "#CBD5E8",
        "#F4CAE4",
        "#E6F5C9",
        "#FFF2AE",
        "#F1E2CC",
        "#CCCCCC",
    ]
    file_color_by_name = {file_name: file_colors[i] for i, (file_name, _) in enumerate(file_specs)}
    text(file_x0 - 0.22, file_y + file_h / 2 - 0.02, "offset", 7.0, "bold", colors["muted"], ha="right")
    for i, (file_name, writes) in enumerate(file_specs):
        fx = file_x0 + i * (file_w + file_gap)
        ax.add_patch(
            plt.Rectangle(
                (fx, file_y - 0.02),
                file_w,
                file_h,
                facecolor=file_color_by_name[file_name],
                edgecolor="#B8C2CC",
                linewidth=1.0,
                alpha=0.82,
            )
        )
        for key, offset_ratio in writes:
            offset_y = file_y + 0.10 + offset_ratio * (file_h - 0.20)
            ax.plot(
                [fx + 0.10 * file_w, fx + 0.90 * file_w],
                [offset_y, offset_y],
                color=process_colors[key],
                linewidth=3.4,
                solid_capstyle="round",
            )
        text(fx + file_w / 2, file_y + file_h + 0.22, file_name, 8.8, "bold", colors["text"])

    r0_x, r0_y = process_centers["P1"]
    coord_y = r0_y + 1.08
    for target_key, rad in [("P2", 0.0), ("PN-1", 0.16), ("PN", 0.24)]:
        target_x, _ = process_centers[target_key]
        curved_arrow(r0_x, coord_y, target_x, coord_y, rad=rad, color=process_colors["P1"], lw=1.1, alpha=0.7)

    for key, (x1, y1), x2 in [
        ("P2", process_centers["P2"], 4.35),
        ("PN-1", process_centers["PN-1"], 7.65),
        ("PN", process_centers["PN"], 9.65),
    ]:
        arrow(x1, y1, x2, shared_y + shared_h, color=process_colors[key], lw=1.15, alpha=0.65)
    ax.text(
        shared_x + shared_w / 2,
        shared_y + shared_h - 0.25,
        "Arquivos Compartilhados",
        fontsize=14,
        fontweight="bold",
        color=colors["process_border"],
        ha="center",
        va="center",
        bbox=dict(facecolor=colors["shared"], edgecolor="none", pad=2.0),
    )

    lustre_x, lustre_y, lustre_w, lustre_h = 0.6, 0.65, 10.8, 2.2
    box(lustre_x, lustre_y, lustre_w, lustre_h, colors["lustre"], colors["lustre_border"])
    text(lustre_x + lustre_w / 2, lustre_y + lustre_h - 0.25, "Sistema de arquivos Lustre", 14, "bold", colors["lustre_border"])
    text(lustre_x + lustre_w / 2, lustre_y + lustre_h - 0.55, "striping distribui blocos coloridos dos arquivos entre OSTs", 9.3, color=colors["muted"], style="italic")

    storage_specs = [
        ("MDS", 1.0),
        ("OST 1", 3.15),
        ("OST 2", 5.25),
        ("OST 3", 7.35),
        ("OST 4", 9.45),
    ]
    stripe_distribution = {
        "OST 1": [("Arq. 1", "Arquivo1"), ("Arq. 5", "Arquivo5")],
        "OST 2": [("Arq. 2", "Arquivo2"), ("Arq. 6", "Arquivo6")],
        "OST 3": [("Arq. 3", "Arquivo3"), ("Arq. 7", "Arquivo7")],
        "OST 4": [("Arq. 4", "Arquivo4"), ("Arq. N", "ArquivoN")],
    }

    for title, x in storage_specs:
        box(x, lustre_y + 0.25, 1.45, 1.15, "white", colors["lustre_border"], lw=1.2)
        text(x + 0.72, lustre_y + 1.15, title, 10.5, "bold", colors["lustre_border"])
        if title == "MDS":
            text(x + 0.72, lustre_y + 0.72, "metadados", 8.0, color=colors["muted"])
            continue

        stripe_specs = [
            (
                stripe_y,
                file_color_by_name[file_name],
                stripe_label,
            )
            for stripe_y, (stripe_label, file_name) in zip(
                [lustre_y + 0.70, lustre_y + 0.38],
                stripe_distribution[title],
            )
        ]
        for stripe_y, stripe_color, stripe_label in stripe_specs:
            box(x + 0.16, stripe_y, 1.13, 0.23, stripe_color, "#B8C2CC", lw=0.8)
            text(x + 0.72, stripe_y + 0.115, stripe_label, 6.8, "bold", colors["text"])

    for target_x in [3.87, 5.97, 8.07, 10.17]:
        arrow(shared_x + shared_w / 2, shared_y, target_x, lustre_y + lustre_h, color=colors["dash"], lw=1.0, alpha=0.7)

    finish(fig, output)


def lustre_architecture_plot(output: str) -> None:
    from matplotlib.patches import FancyBboxPatch

    LC = {
        "client": "#EAF2FB", "client_b": "#2B6CB0",
        "net": "#E8EEF5", "net_b": "#607D8B",
        "mds": "#FCEBEA", "mds_b": "#C53030",
        "mdt": "#F9D5D2",
        "oss": "#E9F7EF", "oss_b": "#2E7D32",
        "ost": "#BFE6C5",
        "text": "#263238", "muted": "#607D8B", "arrow": "#455A64",
    }

    def rbox(ax, x, y, w, h, face, edge, lw=1.8):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=0.10",
                                    facecolor=face, edgecolor=edge, linewidth=lw))

    def tx(ax, x, y, s, size=10, weight="normal", color=None, style="normal"):
        ax.text(x, y, s, fontsize=size, fontweight=weight, ha="center", va="center",
                color=color or LC["text"], style=style)

    def ar(ax, x1, y1, x2, y2, color=None, lw=1.6, style="-|>"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color or LC["arrow"],
                                    linewidth=lw, shrinkA=0, shrinkB=0))

    fig, ax = plt.subplots(figsize=(11.5, 7.2))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 7.2)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    cli_y, cw, ch = 6.05, 1.9, 0.85
    cli_specs = [(0.6, "Cliente 1"), (2.75, "Cliente 2"), (4.9, "..."), (6.55, "Cliente N")]
    cli_cx = []
    for x, label in cli_specs:
        if label == "...":
            tx(ax, x + 0.35, cli_y + ch / 2, "...", 20, "bold", LC["muted"])
            cli_cx.append(x + 0.35)
            continue
        rbox(ax, x, cli_y, cw, ch, LC["client"], LC["client_b"], 2.0)
        tx(ax, x + cw / 2, cli_y + ch / 2, label, 11, "bold", LC["client_b"])
        cli_cx.append(x + cw / 2)
    tx(ax, 9.7, cli_y + ch / 2, "Processos MPI\n(nós de cálculo)", 9.5, "normal", LC["muted"], style="italic")

    net_y, net_h = 4.95, 0.62
    rbox(ax, 0.6, net_y, 9.0, net_h, LC["net"], LC["net_b"], 1.6)
    tx(ax, 5.1, net_y + net_h / 2, "Rede de interconexão de alta velocidade", 12, "bold", LC["net_b"])
    for cx in cli_cx:
        ar(ax, cx, cli_y, cx, net_y + net_h, LC["client_b"], 1.4)

    mds_x, mds_y, mds_w, mds_h = 0.6, 3.05, 2.6, 1.2
    rbox(ax, mds_x, mds_y, mds_w, mds_h, LC["mds"], LC["mds_b"], 2.0)
    tx(ax, mds_x + mds_w / 2, mds_y + mds_h - 0.30, "MDS", 13, "bold", LC["mds_b"])
    tx(ax, mds_x + mds_w / 2, mds_y + 0.32, "Metadata Server\n(namespace, permissões)", 8.6, "normal", LC["muted"])
    mdt_y = 1.35
    rbox(ax, mds_x + 0.45, mdt_y, mds_w - 0.9, 0.85, LC["mdt"], LC["mds_b"], 1.6)
    tx(ax, mds_x + mds_w / 2, mdt_y + 0.43, "MDT\n(metadados)", 9.2, "bold", LC["mds_b"])
    ar(ax, mds_x + mds_w / 2, mds_y, mds_x + mds_w / 2, mdt_y + 0.85)
    ar(ax, mds_x + mds_w / 2, net_y, mds_x + mds_w / 2, mds_y + mds_h, LC["mds_b"], 1.6, style="<|-|>")

    oss_specs = [(3.95, "OSS 1"), (6.05, "OSS 2"), (8.15, "OSS M")]
    oss_w, oss_h, oss_y = 1.85, 1.2, 3.05
    ost_y = 1.35
    for ox, label in oss_specs:
        rbox(ax, ox, oss_y, oss_w, oss_h, LC["oss"], LC["oss_b"], 2.0)
        tx(ax, ox + oss_w / 2, oss_y + oss_h - 0.30, label, 12, "bold", LC["oss_b"])
        tx(ax, ox + oss_w / 2, oss_y + 0.34, "Object Storage\nServer", 8.4, "normal", LC["muted"])
        ar(ax, ox + oss_w / 2, net_y, ox + oss_w / 2, oss_y + oss_h, LC["oss_b"], 1.6, style="<|-|>")
        for dx in [0.12, 1.00]:
            rbox(ax, ox + dx - 0.06, ost_y, 0.82, 0.85, LC["ost"], LC["oss_b"], 1.4)
            tx(ax, ox + dx + 0.35, ost_y + 0.43, "OST", 8.8, "bold", LC["oss_b"])
        ar(ax, ox + oss_w / 2, oss_y, ox + 0.41, ost_y + 0.85)
        ar(ax, ox + oss_w / 2, oss_y, ox + 1.29, ost_y + 0.85)

    tx(ax, 1.9, 2.55, "Caminho de metadados", 9.0, "bold", LC["mds_b"], style="italic")
    tx(ax, 6.95, 0.92, "Caminho de dados (OSS → OST)", 9.0, "bold", LC["oss_b"], style="italic")
    tx(ax, 5.75, 0.55, "Os clientes consultam o MDS para localizar o arquivo e, em seguida, "
       "leem/escrevem os dados diretamente nos OSTs por meio dos OSS.",
       9.2, "normal", LC["muted"], style="italic")

    fig.tight_layout()
    FIGURES_DIR.mkdir(exist_ok=True)
    fig.savefig(FIGURES_DIR / output, dpi=300, bbox_inches="tight")
    plt.close(fig)


def lustre_striping_plot(output: str) -> None:
    from matplotlib.patches import FancyBboxPatch

    LC = {"ost": "#BFE6C5", "ost_b": "#2E7D32", "oss_b": "#2E7D32",
          "text": "#263238", "muted": "#607D8B", "arrow": "#455A64"}

    def rbox(ax, x, y, w, h, face, edge, lw=1.8):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=0.10",
                                    facecolor=face, edgecolor=edge, linewidth=lw))

    def tx(ax, x, y, s, size=10, weight="normal", color=None, style="normal"):
        ax.text(x, y, s, fontsize=size, fontweight=weight, ha="center", va="center",
                color=color or LC["text"], style=style)

    def ar(ax, x1, y1, x2, y2, color=None, lw=1.6, style="-|>"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color or LC["arrow"],
                                    linewidth=lw, shrinkA=0, shrinkB=0))

    fig, ax = plt.subplots(figsize=(11.5, 6.4))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    n_ost = 4
    stripe_colors = ["#4C78A8", "#F58518", "#54A24B", "#E45756"]

    tx(ax, 5.75, 6.05, "Arquivo lógico (visão da aplicação)", 12.5, "bold", LC["text"])
    fx0, fy, sw, sh = 0.9, 5.0, 1.18, 0.78
    n_stripes = 8
    for i in range(n_stripes):
        col = stripe_colors[i % n_ost]
        x = fx0 + i * sw
        rbox(ax, x, fy, sw - 0.06, sh, col, col, 0.0)
        ax.add_patch(plt.Rectangle((x, fy), sw - 0.06, sh, fill=False, edgecolor="white", linewidth=1.4))
        tx(ax, x + (sw - 0.06) / 2, fy + sh / 2, f"stripe {i}", 9.2, "bold", "white")
    ax.annotate("", xy=(fx0 + sw - 0.06, fy - 0.20), xytext=(fx0, fy - 0.20),
                arrowprops=dict(arrowstyle="<|-|>", color=LC["muted"], linewidth=1.3))
    tx(ax, fx0 + (sw - 0.06) / 2, fy - 0.45, "stripe size\n(ex.: 1 MB)", 8.6, "bold", LC["muted"])

    oy, ow, oh = 1.0, 2.25, 1.5
    gap = (11.5 - n_ost * ow) / (n_ost + 1)
    ost_cx = []
    for j in range(n_ost):
        ox = gap + j * (ow + gap)
        rbox(ax, ox, oy, ow, oh, LC["ost"], LC["ost_b"], 2.0)
        tx(ax, ox + ow / 2, oy + oh - 0.28, f"OST {j}", 12, "bold", LC["oss_b"])
        ost_cx.append(ox + ow / 2)
        mine = [i for i in range(n_stripes) if i % n_ost == j]
        bw = 0.62
        bx0 = ox + (ow - len(mine) * bw - (len(mine) - 1) * 0.12) / 2
        for k, i in enumerate(mine):
            bx = bx0 + k * (bw + 0.12)
            rbox(ax, bx, oy + 0.28, bw, 0.55, stripe_colors[j], stripe_colors[j], 0.0)
            tx(ax, bx + bw / 2, oy + 0.28 + 0.275, f"{i}", 9.0, "bold", "white")

    for i in range(n_ost):
        sx = fx0 + i * sw + (sw - 0.06) / 2
        ar(ax, sx, fy, ost_cx[i], oy + oh, stripe_colors[i], 1.7)

    tx(ax, 5.75, 0.45, "stripe count = 4: os stripes do arquivo são distribuídos de forma "
       "circular (round-robin) entre os OSTs, permitindo E/S paralela.",
       9.2, "normal", LC["muted"], style="italic")

    fig.tight_layout()
    FIGURES_DIR.mkdir(exist_ok=True)
    fig.savefig(FIGURES_DIR / output, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    sd_current = read_csv(PATHS["sd_current"], max_nodes=16)
    sd_mpiio = read_csv(PATHS["sd_mpiio"], max_nodes=16)
    aws_current = read_csv(PATHS["aws_current"])
    aws_mpiio = read_csv(PATHS["aws_mpiio"])

    bandwidth_plot(sd_current, sd_mpiio, "Banda_SDumont.png")
    time_plot(sd_current, sd_mpiio, "Tempo_execucao_SDumont.png")
    message_size_plot(sd_current, sd_mpiio, "EnvioPorTamanho_SDumont.png")

    bandwidth_plot(aws_current, aws_mpiio, "Banda_AWS.png")
    time_plot(aws_current, aws_mpiio, "Tempo_execucao_AWS.png")
    message_size_plot(aws_current, aws_mpiio, "EnvioPorTamanho_AWS.png")
    message_count_by_size_plot("histograma_mensagens.png")
    sddp_timeline_plot("SDDP_timeline_MPIIO.png")

    lustre_architecture_plot("Lustre_arquitetura.png")
    lustre_striping_plot("Lustre_striping.png")
