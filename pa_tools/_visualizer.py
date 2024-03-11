import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

plt.rcParams["font.family"] = "AppleGothic"


def plot_fig(ohlcv, rp, rvp, tdp, tdvp):
    fig = plt.figure(figsize=(12, 6))
    gs = gridspec.GridSpec(2, 3, width_ratios=[2, 1, 1], height_ratios=[1, 1])

    # 왼쪽 큰 그림
    ax1 = plt.subplot(gs[:, 0])
    ax1.plot(ohlcv.index, ohlcv["close"], label="Close", linewidth=5)
    ax1.plot(ohlcv.index, ohlcv["high"], label="High", linestyle="--", linewidth=5)
    ax1.plot(ohlcv.index, ohlcv["low"], label="Low", linestyle="-.", linewidth=5)
    ax1.legend(loc="upper left")

    ax2 = ax1.twinx()
    ax2.bar(ohlcv.index, ohlcv["volume"], label="Volume", alpha=0.5, color="grey")
    ax2.legend(loc="upper right")
    ax1.set_title("Main")

    # 오른쪽 상단 첫 번째 작은 그림
    ax2 = plt.subplot(gs[0, 1])
    sns.kdeplot(rp, fill=True, ax=ax2)
    ax2.set_title("기본")

    # 오른쪽 상단 두 번째 작은 그림
    ax3 = plt.subplot(gs[0, 2])
    sns.kdeplot(rvp, fill=True, ax=ax3)
    ax3.set_title("거래량 가중")

    # 오른쪽 하단 첫 번째 작은 그림
    ax4 = plt.subplot(gs[1, 1])
    sns.kdeplot(tdp, fill=True, ax=ax4)
    ax4.set_title("시간 가중")

    # 오른쪽 하단 두 번째 작은 그림
    ax5 = plt.subplot(gs[1, 2])
    sns.kdeplot(tdvp, fill=True, ax=ax5)
    ax5.set_title("시간/거래량 가중")

    plt.tight_layout()
    plt.show()
