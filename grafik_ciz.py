import matplotlib.pyplot as plt
import pandas as pd

def grafik_ciz():
    sirketler = ["AAPL", "MSFT", "TSLA", "AMZN"]
    
    plt.figure(figsize=(10, 6))
    
    for sembol in sirketler:
        df = pd.read_csv(f"{sembol}_oranlar.csv", index_col=0)
        yil_sirasi = range(1, len(df) + 1)  # 1, 2, 3, 4 şeklinde göreceli sıra
        plt.plot(yil_sirasi, df["Net Kâr Marjı (%)"], marker="o", label=sembol)
    
    plt.title("Şirketlerin Net Kâr Marjı Karşılaştırması")
    plt.xlabel("Yıl Sırası (1 = en eski, 4 = en yeni)")
    plt.ylabel("Net Kâr Marjı (%)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks([1, 2, 3, 4])
    plt.tight_layout()
    plt.savefig("kar_marji_karsilastirma.png")
    plt.show()

if __name__ == "__main__":
    grafik_ciz()