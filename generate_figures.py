from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent


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
    fig.savefig(ROOT / output, dpi=300, bbox_inches="tight")
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


if __name__ == "__main__":
    main()
