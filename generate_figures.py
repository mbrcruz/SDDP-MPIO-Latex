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


def sddp_timeline_plot(output: str) -> None:
    fig, ax = plt.subplots(figsize=(12.4, 5.6))
    ax.set_xlim(-0.25, 11.1)
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
        ("Processo 0", 3.3, 0.18, 0.72, [(1, 1.05), (5, 3.15), (9, 0.9)]),
        ("Processo 1", 2.35, 0.46, 0.28, [(2, 2.85), (6, 0.95), (10, 3.05)]),
        ("Processo 2", 1.4, 0.68, 0.44, [(3, 3.2), (7, 1.1), (11, 2.55)]),
        ("Processo N", 0.45, 0.24, 0.84, [(4, 0.9), (8, 3.35), ("X", 1.25)]),
    ]
    coord_start_x = 0.15
    coord_width = 0.66
    final_coord_end_x = 10.55
    io_widths = [0.34, 0.38, 0.36]

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

    rect = plt.Rectangle(
        (coord_start_x, 0.0),
        coord_width,
        3.75,
        facecolor=colors["coord"],
        edgecolor="white",
        linewidth=1.4,
        zorder=2,
    )
    ax.add_patch(rect)
    ax.text(
        coord_start_x + coord_width / 2,
        1.88,
        "Coordenação MPI-IO",
        ha="center",
        va="center",
        fontsize=9.5,
        color=colors["text"],
        weight="bold",
        rotation=90,
        zorder=4,
    )

    for process, y, initial_comm_width, final_comm_width, tasks in processes:
        ax.hlines(y, 0.0, 9.75, color=colors["line"], linewidth=2.0, zorder=1)
        ax.text(-0.08, y, process, ha="right", va="center", fontsize=10.5, color=colors["text"], weight="bold")
        x = coord_start_x + coord_width
        block(x, y, initial_comm_width, 0.3, colors["comm"], "", size=8.5)
        x += initial_comm_width
        for idx, (scenario, compute_width) in enumerate(tasks):
            label = f"Cenário {scenario}" if compute_width < 1.2 else f"Resolvendo cenário {scenario}"
            label_size = 6.2 if compute_width < 1.2 else 7.4 if compute_width < 1.6 else 8.8
            block(x, y, compute_width, 0.5, colors["resolve"], label, size=label_size)
            x += compute_width
            block(x, y, io_widths[idx], 0.34, colors["io"], "E/S", size=8.5)
            x += io_widths[idx]
        block(x, y, final_comm_width, 0.3, colors["comm"], "", size=8.5)
        x += final_comm_width
        block(x, y, final_coord_end_x - x, 0.5, colors["coord"], "", size=8.5)

    legend_y = 4.28
    legend_items = [
        (0.95, colors["resolve"], "Resolvendo cenário X"),
        (3.35, colors["io"], "E/S"),
        (4.55, colors["coord"], "Coordenação MPI-IO"),
    ]
    for x, color, label in legend_items:
        ax.add_patch(plt.Rectangle((x, legend_y - 0.13), 0.28, 0.26, facecolor=color, edgecolor="none"))
        ax.text(x + 0.38, legend_y, label, ha="left", va="center", fontsize=10.4, color=colors["text"])

    ax.text(
        4.9,
        4.58,
        "Linha do tempo da simulação final do SDDP com MPI-IO",
        ha="center",
        va="center",
        fontsize=14,
        weight="bold",
        color=colors["text"],
    )

    finish(fig, output)


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


if __name__ == "__main__":
    main()
