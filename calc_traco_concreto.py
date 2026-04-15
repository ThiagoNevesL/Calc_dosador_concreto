import tkinter as tk
from tkinter import ttk, messagebox

class CalculadoraTracoConcreto:
    def __init__(self, root):
        self.root = root
        self.root.title("Dosador de Concreto")
        self.root.geometry("750x750")
        self.root.resizable(True, True)

        # estilos
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"))
        style.configure("TLabelframe", font=("Arial", 10, "bold"))
        style.configure("TLabelframe.Label", font=("Arial", 10, "bold"))

        # entrada de dados 
        frame_fck = ttk.LabelFrame(root, text="1. Resistência do projeto (Fck)", padding=10)
        frame_fck.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        ttk.Label(frame_fck, text="Fck (MPa):").grid(row=0, column=0, sticky="w")
        self.entry_fck = ttk.Entry(frame_fck, width=10, font=("Arial", 11))
        self.entry_fck.grid(row=0, column=1, padx=5, sticky="w")
        self.entry_fck.insert(0, "30")
        btn_help_fck = ttk.Button(frame_fck, text="?", width=2, command=self.explicar_fck)
        btn_help_fck.grid(row=0, column=2, padx=5)

        # slump
        frame_slump = ttk.LabelFrame(root, text="2. Consistência (Abatimento)", padding=10)
        frame_slump.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        ttk.Label(frame_slump, text="Arraste o controle:").grid(row=0, column=0, sticky="w")
        self.slider_abat = tk.Scale(frame_slump, from_=10, to=120, orient="horizontal",
                                    length=350, command=self.atualizar_texto_abatimento)
        self.slider_abat.set(80)
        self.slider_abat.grid(row=0, column=1, padx=5, sticky="ew")
        self.label_classificacao = ttk.Label(frame_slump, text="Concreto plástico (média)",
                                             font=("Arial", 9, "italic"))
        self.label_classificacao.grid(row=0, column=2, padx=10)
        btn_help_slump = ttk.Button(frame_slump, text="?", width=2, command=self.explicar_trabalhabilidade)
        btn_help_slump.grid(row=0, column=3, padx=5)

        # materiais
        frame_materiais = ttk.LabelFrame(root, text="3. Escolha os materiais", padding=10)
        frame_materiais.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        ttk.Label(frame_materiais, text="Tipo de Cimento:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_cimento = ttk.Combobox(frame_materiais, values=[
            "CP II - Cimento Portland Composto (padrão)",
            "CP III - Alto Forno (mais durável)",
            "CP IV - Pozolânico (menor calor)",
            "CP V-ARI - Alta Resistência Inicial"
        ], state="readonly", width=40)
        self.combo_cimento.current(0)
        self.combo_cimento.grid(row=0, column=1, sticky="w", pady=5)
        btn_help_cim = ttk.Button(frame_materiais, text="?", width=2, command=self.explicar_cimento)
        btn_help_cim.grid(row=0, column=2, padx=5)

        ttk.Label(frame_materiais, text="Tipo de Brita (tamanho):").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_brita = ttk.Combobox(frame_materiais, values=[
            "Brita 0 (Dmáx = 9,5 mm) - Concreto aparente",
            "Brita 1 (Dmáx = 19 mm) - Padrão para estruturas",
            "Brita 2 (Dmáx = 25 mm) - Concreto massa"
        ], state="readonly", width=40)
        self.combo_brita.current(1)
        self.combo_brita.grid(row=1, column=1, sticky="w", pady=5)
        btn_help_brita = ttk.Button(frame_materiais, text="?", width=2, command=self.explicar_brita)
        btn_help_brita.grid(row=1, column=2, padx=5)

        ttk.Label(frame_materiais, text="Tipo de Areia:").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_areia = ttk.Combobox(frame_materiais, values=[
            "Areia Fina (MF < 2,0) - Acabamento liso",
            "Areia Média (2,0 ≤ MF ≤ 2,8) - Uso geral",
            "Areia Grossa (MF > 2,8) - Maior resistência"
        ], state="readonly", width=40)
        self.combo_areia.current(1)
        self.combo_areia.grid(row=2, column=1, sticky="w", pady=5)
        btn_help_areia = ttk.Button(frame_materiais, text="?", width=2, command=self.explicar_areia)
        btn_help_areia.grid(row=2, column=2, padx=5)

        # botão calcular
        self.btn_calcular = ttk.Button(root, text="Calcular Traço do Concreto",
                                       command=self.calcular_traco, style="Accent.TButton")
        self.btn_calcular.grid(row=3, column=0, pady=20)

        # resultados
        frame_resultado = ttk.LabelFrame(root, text="Receita do Concreto", padding=10)
        frame_resultado.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        self.resultado_cimento = ttk.Label(frame_resultado, text="Cimento: -- kg/m³", font=("Arial", 10))
        self.resultado_cimento.grid(row=0, column=0, sticky="w", pady=2)
        self.resultado_areia = ttk.Label(frame_resultado, text="Areia: -- kg/m³", font=("Arial", 10))
        self.resultado_areia.grid(row=1, column=0, sticky="w", pady=2)
        self.resultado_brita = ttk.Label(frame_resultado, text="Brita: -- kg/m³", font=("Arial", 10))
        self.resultado_brita.grid(row=2, column=0, sticky="w", pady=2)
        self.resultado_agua = ttk.Label(frame_resultado, text="Água: -- L/m³", font=("Arial", 10))
        self.resultado_agua.grid(row=3, column=0, sticky="w", pady=2)
        self.resultado_ac = ttk.Label(frame_resultado, text="Relação Água/Cimento: --",
                                      font=("Arial", 10, "bold"))
        self.resultado_ac.grid(row=4, column=0, sticky="w", pady=2)
        self.resultado_obra = ttk.Label(frame_resultado,
                                        text="Traço para 1 saco de cimento (50 kg):\n--",
                                        font=("Arial", 10))
        self.resultado_obra.grid(row=5, column=0, sticky="w", pady=15)

        # ajuste de grid
        root.columnconfigure(0, weight=1)
        frame_slump.columnconfigure(1, weight=1)

    # essas funções são só pra dar ajuda ao usuário 
    def atualizar_texto_abatimento(self, valor):
        v = int(valor)
        if v <= 40:
            texto = "Concreto seco (pouco fluido)\nPisos e calçadas"
        elif v <= 90:
            texto = "Concreto plástico (média)\nVigas, pilares, lajes"
        else:
            texto = "Concreto fluido (auto-adensável)\nBombeamento"
        self.label_classificacao.config(text=texto)

    def explicar_fck(self):
        messagebox.showinfo("Fck", "Resistência característica aos 28 dias.\n"
                            "20 MPa: calçadas | 25-30: residências | >35: especiais\n"
                            "O programa já adiciona 4 MPa de segurança.")

    def explicar_trabalhabilidade(self):
        messagebox.showinfo("Consistência", "10-40mm: seco (vibração)\n50-90mm: plástico (geral)\n100-120mm: fluido (bombeamento)")

    def explicar_cimento(self):
        messagebox.showinfo("Cimento", "CP II: geral\nCP III: durável\nCP IV: baixo calor\nCP V-ARI: alta resistência inicial")

    def explicar_brita(self):
        messagebox.showinfo("Brita", "Brita0 (9.5mm): acabamento\nBrita1 (19mm): estruturas\nBrita2 (25mm): massas")

    def explicar_areia(self):
        messagebox.showinfo("Areia", "Fina: mais água, bom acabamento\nMédia: equilíbrio\nGrossa: menos água, mais resistência")

    # cálculos 
    def calcular_traco(self):
        # validação básica
        try:
            fck = float(self.entry_fck.get())
            if fck <= 0: raise ValueError
        except:
            messagebox.showerror("Erro", "Fck tem que ser número positivo.")
            return

        abat = self.slider_abat.get()
        cim_idx = self.combo_cimento.current()
        brita_idx = self.combo_brita.current()
        areia_idx = self.combo_areia.current()

        # resistência de dosagem
        fcj = fck + 4.0   # desvio padrão 4 MPa

        # relação a/c
        ac = self._relacao_ac(fcj, cim_idx)

        # consumo de água
        agua = self._consumo_agua(abat, brita_idx, areia_idx)

        cimento = agua / ac

        # massas específicas
        dens_cim = 3100.0
        if cim_idx == 1:   # CP III é mais leve
            dens_cim = 3000.0
        elif cim_idx == 3: # CP V-ARI é mais denso
            dens_cim = 3150.0
        dens_areia = 2650.0
        dens_brita = 2700.0

        # volume de brita compactada (tabela ABCP)
        vol_brita_tab = [
            [0.68, 0.72, 0.76],
            [0.66, 0.70, 0.74],
            [0.64, 0.68, 0.72]
        ]
        vol_brita = vol_brita_tab[areia_idx][brita_idx]
        massa_brita = vol_brita * 1500.0   # massa unitária compactada

        # volumes absolutos
        vol_agua = agua / 1000.0
        vol_cim = cimento / dens_cim
        vol_brita_abs = massa_brita / dens_brita

        # ar aprisionado (aproximação)
        ar = [0.025, 0.02, 0.015][brita_idx]

        vol_areia = 1.0 - (vol_cim + vol_agua + vol_brita_abs + ar)
        if vol_areia < 0:
            messagebox.showerror("Erro", "Volume de areia negativo. Tente diminuir o Fck ou o abatimento.")
            return

        massa_areia = vol_areia * dens_areia

        # atualizar interface
        self.resultado_cimento.config(text=f"Cimento: {cimento:.1f} kg/m³")
        self.resultado_areia.config(text=f"Areia: {massa_areia:.1f} kg/m³")
        self.resultado_brita.config(text=f"Brita: {massa_brita:.1f} kg/m³")
        self.resultado_agua.config(text=f"Água: {agua:.1f} L/m³")
        self.resultado_ac.config(text=f"Relação Água/Cimento: {ac:.2f}")

        # traço unitário e para saco de 50kg
        traco_a = massa_areia / cimento
        traco_b = massa_brita / cimento
        saco = 50.0
        areia_saco = traco_a * saco
        brita_saco = traco_b * saco
        agua_saco = (agua / cimento) * saco

        texto = (f"Traço para 1 saco (50 kg):\n"
                 f"• Areia: {areia_saco:.1f} kg  (~ {areia_saco/30:.1f} baldes 20L)\n"
                 f"• Brita: {brita_saco:.1f} kg  (~ {brita_saco/30:.1f} baldes 20L)\n"
                 f"• Água: {agua_saco:.1f} litros\n\n"
                 f"Proporção: 1 : {traco_a:.2f} : {traco_b:.2f} (a/c={ac:.2f})")
        self.resultado_obra.config(text=texto)

    #  funções auxiliares internas 
    def _relacao_ac(self, fcj, tipo_cim):
        # tabela da ABCP para CP II
        fck_ref = [15, 20, 25, 30, 35, 40, 45, 50]
        ac_ref = [0.80, 0.70, 0.60, 0.55, 0.50, 0.45, 0.40, 0.35]

        # ajuste pra outros cimentos (fatores empíricos)
        fator = [1.00, 1.02, 0.98, 0.95][tipo_cim]

        if fcj <= fck_ref[0]:
            ac = ac_ref[0]
        elif fcj >= fck_ref[-1]:
            ac = ac_ref[-1]
        else:
            for i in range(len(fck_ref)-1):
                if fck_ref[i] <= fcj <= fck_ref[i+1]:
                    ac = ac_ref[i] + (fcj - fck_ref[i]) * (ac_ref[i+1] - ac_ref[i]) / (fck_ref[i+1] - fck_ref[i])
                    break
            else:
                ac = 0.55   # fallback
        return ac * fator

    def _consumo_agua(self, abat, brita_idx, areia_idx):
        base = 195.0
        if abat <= 40:
            agua = base - 10
        elif abat <= 90:
            agua = base + (abat - 60) * 0.25
        else:
            agua = base + 15

        # brita 0 pede mais água, brita 2 menos
        ajuste_b = [8, 0, -8][brita_idx]
        # areia fina também, grossa menos
        ajuste_a = [6, 0, -6][areia_idx]

        agua += ajuste_b + ajuste_a
        # limite razoável
        if agua < 160: agua = 160
        if agua > 240: agua = 240
        return agua

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraTracoConcreto(root)
    root.mainloop()
