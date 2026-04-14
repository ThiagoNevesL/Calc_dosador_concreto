# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox

class CalculadoraTracoConcreto:
    """
    Aplicativo para dosagem de concreto pelo Método ABCP.
    Permite ao usuário escolher:
      - Tipo de cimento
      - Tipo de brita (Dmáx)
      - Tipo de areia (módulo de finura)
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Dosador de Concreto - Método ABCP")
        self.root.geometry("750x750")
        self.root.resizable(True, True)

        # Estilos visuais
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"))
        style.configure("TLabelframe", font=("Arial", 10, "bold"))
        style.configure("TLabelframe.Label", font=("Arial", 10, "bold"))

        # =====================================================================
        # 1. ENTRADA DE DADOS
        # =====================================================================

        # ---------- Resistência (Fck) ----------
        frame_fck = ttk.LabelFrame(root, text="1. Resistência do projeto (Fck)", padding=10)
        frame_fck.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        ttk.Label(frame_fck, text="Fck (MPa):").grid(row=0, column=0, sticky="w")
        self.entry_fck = ttk.Entry(frame_fck, width=10, font=("Arial", 11))
        self.entry_fck.grid(row=0, column=1, padx=5, sticky="w")
        self.entry_fck.insert(0, "30")

        btn_help_fck = ttk.Button(frame_fck, text="?", width=2, command=self.explicar_fck)
        btn_help_fck.grid(row=0, column=2, padx=5)

        # ---------- Consistência (Slider) ----------
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

        btn_help_slump = ttk.Button(frame_slump, text="?", width=2,
                                    command=self.explicar_trabalhabilidade)
        btn_help_slump.grid(row=0, column=3, padx=5)

        # ---------- NOVOS CAMPOS: MATERIAIS ----------
        frame_materiais = ttk.LabelFrame(root, text="3. Escolha os materiais", padding=10)
        frame_materiais.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # --- Tipo de Cimento ---
        ttk.Label(frame_materiais, text="Tipo de Cimento:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_cimento = ttk.Combobox(frame_materiais, values=[
            "CP II – Cimento Portland Composto (padrão)",
            "CP III – Alto Forno (mais durável)",
            "CP IV – Pozolânico (menor calor)",
            "CP V-ARI – Alta Resistência Inicial"
        ], state="readonly", width=40)
        self.combo_cimento.current(0)   # Seleciona o primeiro por padrão
        self.combo_cimento.grid(row=0, column=1, sticky="w", pady=5)

        btn_help_cim = ttk.Button(frame_materiais, text="?", width=2,
                                  command=self.explicar_cimento)
        btn_help_cim.grid(row=0, column=2, padx=5)

        # --- Tipo de Brita (Dmáx) ---
        ttk.Label(frame_materiais, text="Tipo de Brita (tamanho):").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_brita = ttk.Combobox(frame_materiais, values=[
            "Brita 0 (Dmáx = 9,5 mm) – Concreto aparente",
            "Brita 1 (Dmáx = 19 mm) – Padrão para estruturas",
            "Brita 2 (Dmáx = 25 mm) – Concreto massa"
        ], state="readonly", width=40)
        self.combo_brita.current(1)   # Brita 1 como padrão
        self.combo_brita.grid(row=1, column=1, sticky="w", pady=5)

        btn_help_brita = ttk.Button(frame_materiais, text="?", width=2,
                                    command=self.explicar_brita)
        btn_help_brita.grid(row=1, column=2, padx=5)

        # --- Tipo de Areia (Módulo de Finura) ---
        ttk.Label(frame_materiais, text="Tipo de Areia:").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_areia = ttk.Combobox(frame_materiais, values=[
            "Areia Fina (MF < 2,0) – Acabamento liso",
            "Areia Média (2,0 ≤ MF ≤ 2,8) – Uso geral",
            "Areia Grossa (MF > 2,8) – Maior resistência"
        ], state="readonly", width=40)
        self.combo_areia.current(1)   # Areia média padrão
        self.combo_areia.grid(row=2, column=1, sticky="w", pady=5)

        btn_help_areia = ttk.Button(frame_materiais, text="?", width=2,
                                    command=self.explicar_areia)
        btn_help_areia.grid(row=2, column=2, padx=5)

        # ---------- Botão de Ação ----------
        self.btn_calcular = ttk.Button(root, text="Calcular Traço do Concreto",
                                       command=self.calcular_traco, style="Accent.TButton")
        self.btn_calcular.grid(row=3, column=0, pady=20)

        # =====================================================================
        # 4. RESULTADO
        # =====================================================================
        frame_resultado = ttk.LabelFrame(root, text="📊 Receita do Concreto", padding=10)
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

        # Ajuste de expansão
        root.columnconfigure(0, weight=1)
        frame_slump.columnconfigure(1, weight=1)

    # =========================================================================
    # FUNÇÕES DE APOIO (INTERFACE E EXPLICAÇÕES)
    # =========================================================================
    def atualizar_texto_abatimento(self, valor):
        abat = int(valor)
        if abat <= 40:
            texto = "Concreto seco (pouco fluido)\nPisos e calçadas"
        elif abat <= 90:
            texto = "Concreto plástico (média)\nVigas, pilares, lajes"
        else:
            texto = "Concreto fluido (auto-adensável)\nBombeamento"
        self.label_classificacao.config(text=texto)

    def explicar_fck(self):
        messagebox.showinfo("Fck",
            "Resistência característica do concreto aos 28 dias.\n"
            "Valores comuns:\n"
            "• 20 MPa – calçadas\n"
            "• 25-30 MPa – residências e prédios\n"
            "• 35+ MPa – obras especiais\n"
            "O programa adiciona 4 MPa de segurança.")

    def explicar_trabalhabilidade(self):
        messagebox.showinfo("Consistência",
            "Mede a fluidez do concreto fresco.\n"
            "• 10-40 mm: seco, exige vibração\n"
            "• 50-90 mm: plástico, uso geral\n"
            "• 100-120 mm: fluido, fácil bombear")

    def explicar_cimento(self):
        messagebox.showinfo("Tipo de Cimento",
            "CP II: Uso geral, mais comum.\n"
            "CP III: Maior durabilidade em ambientes agressivos.\n"
            "CP IV: Menor calor de hidratação, bom para grandes volumes.\n"
            "CP V-ARI: Alta resistência inicial, desforma rápida.")

    def explicar_brita(self):
        messagebox.showinfo("Tipo de Brita",
            "Brita 0: Pedrisco (9,5 mm), para acabamentos finos.\n"
            "Brita 1: (19 mm), padrão para estruturas armadas.\n"
            "Brita 2: (25 mm), concreto massa (fundações).")

    def explicar_areia(self):
        messagebox.showinfo("Tipo de Areia",
            "Areia fina: Mais água, melhor acabamento.\n"
            "Areia média: Equilíbrio entre trabalhabilidade e resistência.\n"
            "Areia grossa: Menos água, concreto mais resistente.")

    # =========================================================================
    # 2. PROCESSAMENTO (MÉTODO ABCP)
    # =========================================================================
    def calcular_traco(self):
        # Validação do Fck
        try:
            fck = float(self.entry_fck.get())
            if fck <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Digite um número positivo para o Fck.")
            return

        abatimento = self.slider_abat.get()

        # ---- Leitura das escolhas dos materiais ----
        # Tipo de cimento: índice 0=CP II, 1=CP III, 2=CP IV, 3=CP V
        idx_cim = self.combo_cimento.current()
        # Tipo de brita: 0=Brita 0 (9,5mm), 1=Brita 1 (19mm), 2=Brita 2 (25mm)
        idx_brita = self.combo_brita.current()
        # Tipo de areia: 0=Fina, 1=Média, 2=Grossa
        idx_areia = self.combo_areia.current()

        # ---- 2.1 Resistência de dosagem (Fcj) ----
        desvio_padrao = 4.0
        fcj = fck + desvio_padrao

        # ---- 2.2 Relação Água/Cimento (a/c) considerando o tipo de cimento ----
        ac = self.calcular_relacao_ac(fcj, idx_cim)

        # ---- 2.3 Consumo de água (L/m³) dependendo do abatimento, brita e areia ----
        agua_lm3 = self.calcular_consumo_agua(abatimento, idx_brita, idx_areia)

        # ---- 2.4 Consumo de cimento ----
        cimento_kgm3 = agua_lm3 / ac

        # ---- 2.5 Massas específicas (podem variar ligeiramente com o tipo) ----
        # Cimento: todos em torno de 3100 kg/m³, CP III um pouco menor (3000)
        dens_cimento = 3100.0
        if idx_cim == 1:   # CP III (alto forno)
            dens_cimento = 3000.0
        elif idx_cim == 3: # CP V-ARI
            dens_cimento = 3150.0

        dens_areia = 2650.0   # Areia quartzosa típica
        dens_brita = 2700.0   # Brita granítica

        # ---- 2.6 Volume de brita compactada (m³/m³) - tabela ABCP ----
        # Depende do Dmáx da brita e do módulo de finura da areia.
        # Valores típicos (m³ de brita compactada por m³ de concreto):
        # MF areia / Brita 0 / Brita 1 / Brita 2
        # Fina     : 0,68 / 0,72 / 0,76
        # Média    : 0,66 / 0,70 / 0,74
        # Grossa   : 0,64 / 0,68 / 0,72
        tabela_vol_brita = [
            [0.68, 0.72, 0.76],   # Areia fina
            [0.66, 0.70, 0.74],   # Areia média
            [0.64, 0.68, 0.72]    # Areia grossa
        ]
        vol_brita_compactado = tabela_vol_brita[idx_areia][idx_brita]

        # Massa unitária compactada da brita ≈ 1500 kg/m³
        massa_brita_kgm3 = vol_brita_compactado * 1500.0

        # Volumes reais
        vol_agua = agua_lm3 / 1000.0
        vol_cimento = cimento_kgm3 / dens_cimento
        vol_brita = massa_brita_kgm3 / dens_brita

        # Teor de ar aprisionado (estimado) varia com Dmáx:
        # Brita 0: 2,5%, Brita 1: 2,0%, Brita 2: 1,5%
        ar_aprisionado = [0.025, 0.02, 0.015][idx_brita]

        # Volume de areia = 1 m³ - somatório dos demais
        vol_areia = 1.0 - (vol_cimento + vol_agua + vol_brita + ar_aprisionado)
        if vol_areia < 0:
            messagebox.showerror("Erro de Cálculo",
                                 "Volume de areia negativo. Tente reduzir o Fck ou o abatimento.")
            return

        massa_areia_kgm3 = vol_areia * dens_areia

        # ---- Atualização dos resultados ----
        self.resultado_cimento.config(text=f"Cimento: {cimento_kgm3:.1f} kg/m³")
        self.resultado_areia.config(text=f"Areia: {massa_areia_kgm3:.1f} kg/m³")
        self.resultado_brita.config(text=f"Brita: {massa_brita_kgm3:.1f} kg/m³")
        self.resultado_agua.config(text=f"Água: {agua_lm3:.1f} L/m³")
        self.resultado_ac.config(text=f"Relação Água/Cimento: {ac:.2f}")

        # Traço unitário
        traco_areia = massa_areia_kgm3 / cimento_kgm3
        traco_brita = massa_brita_kgm3 / cimento_kgm3

        # Para 1 saco de 50 kg
        saco = 50.0
        areia_saco = traco_areia * saco
        brita_saco = traco_brita * saco
        agua_saco = (agua_lm3 / cimento_kgm3) * saco

        texto_obra = (
            f"Traço para 1 saco de cimento (50 kg):\n"
            f"• Areia: {areia_saco:.1f} kg  (~ {areia_saco/30:.1f} baldes de 20L)\n"
            f"• Brita: {brita_saco:.1f} kg  (~ {brita_saco/30:.1f} baldes de 20L)\n"
            f"• Água: {agua_saco:.1f} litros\n\n"
            f"Proporção em massa: 1 : {traco_areia:.2f} : {traco_brita:.2f} (a/c = {ac:.2f})"
        )
        self.resultado_obra.config(text=texto_obra)

    # -------------------------------------------------------------------------
    # Relação Água/Cimento ajustada por tipo de cimento
    # -------------------------------------------------------------------------
    @staticmethod
    def calcular_relacao_ac(fcj, idx_cim):
        # Curva base para CP II (índice 0)
        tabela_fcj = [15, 20, 25, 30, 35, 40, 45, 50]
        tabela_ac_base = [0.80, 0.70, 0.60, 0.55, 0.50, 0.45, 0.40, 0.35]

        # Fatores multiplicativos para outros cimentos (em relação ao CP II)
        # CP III permite um a/c ligeiramente maior para mesma resistência?
        # Na verdade, a curva é própria; aqui simplificamos com fatores.
        fatores = [1.00, 1.02, 0.98, 0.95]   # CP II, CP III, CP IV, CP V-ARI
        fator = fatores[idx_cim]

        # Interpolação linear da tabela base
        if fcj <= tabela_fcj[0]:
            ac = tabela_ac_base[0]
        elif fcj >= tabela_fcj[-1]:
            ac = tabela_ac_base[-1]
        else:
            for i in range(len(tabela_fcj)-1):
                if tabela_fcj[i] <= fcj <= tabela_fcj[i+1]:
                    x1, x2 = tabela_fcj[i], tabela_fcj[i+1]
                    y1, y2 = tabela_ac_base[i], tabela_ac_base[i+1]
                    ac = y1 + (fcj - x1) * (y2 - y1) / (x2 - x1)
                    break
            else:
                ac = 0.55   # fallback

        return ac * fator

    # -------------------------------------------------------------------------
    # Consumo de água (L/m³) dependendo do abatimento, Dmáx e MF da areia
    # -------------------------------------------------------------------------
    @staticmethod
    def calcular_consumo_agua(abatimento, idx_brita, idx_areia):
        # Tabela base para Brita 1 e Areia Média (abatimento 40-60 -> 200 L)
        # Ajustes:
        # - Para cada aumento de 20 mm no abatimento, +5 L
        # - Brita 0: +5 L; Brita 2: -5 L (em relação à brita 1)
        # - Areia fina: +5 L; Areia grossa: -5 L (em relação à média)

        # Consumo base (abatimento 60 mm, brita 1, areia média)
        agua_base = 195.0

        # Ajuste por abatimento
        if abatimento <= 40:
            agua = agua_base - 10
        elif abatimento <= 90:
            agua = agua_base + (abatimento - 60) * 0.25   # ~5 L a cada 20 mm
        else:
            agua = agua_base + 15

        # Ajuste por tipo de brita (Dmáx)
        # Brita 0 (índice 0): +8 L; Brita 2 (índice 2): -8 L
        ajuste_brita = [8, 0, -8][idx_brita]

        # Ajuste por tipo de areia (MF)
        ajuste_areia = [6, 0, -6][idx_areia]   # Fina: +6 L; Grossa: -6 L

        agua += ajuste_brita + ajuste_areia
        return max(160, min(240, agua))   # Limita em faixa razoável

# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraTracoConcreto(root)
    root.mainloop()