from datetime import datetime
import io
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit as st

st.set_page_config(
    page_title="Suivi de Croissance", page_icon="📈", layout="centered"
)

st.title("📈 Suivi de Croissance & Santé")
st.write(
    "Entrez les mesures de l'enfant pour visualiser ses courbes officielles"
    " (style carnet de santé) et télécharger le PDF complet."
)

# --- FORMULAIRE DE SAISIE ---
with st.form("form_saisie"):
  st.subheader("Informations de l'enfant")
  nom = st.text_input("Nom de l'enfant", "Mon Enfant")
  sexe = st.selectbox("Sexe", ["Garçon", "Fille"])
  date_naiss_str = st.text_input("Date de naissance (JJ/MM/AAAA)", "15/06/2020")

  col1, col2 = st.columns(2)
  with col1:
    poids = st.number_input("Poids actuel (kg)", value=16.5, step=0.1)
  with col2:
    taille = st.number_input("Taille actuelle (cm)", value=105.0, step=0.5)

  btn_valider = st.form_submit_button("Générer les graphiques et le PDF")

if btn_valider:
  try:
    # Calculs
    date_naiss = datetime.strptime(date_naiss_str, "%d/%m/%Y")
    age_jours = (datetime.now() - date_naiss).days
    age_ans = round(age_jours / 365.25, 2)
    taille_m = taille / 100.0
    imc = round(poids / (taille_m**2), 2)

    st.info(
        f"**{nom}** ({sexe}) — Âge : {age_ans} ans | Taille : {taille} cm |"
        f" Poids : {poids} kg | IMC : {imc}"
    )

    # Données de référence (0 à 18 ans)
    ages_ref = np.linspace(0, 18, 19)

    if sexe == "Garçon":
      t_p3 = [
          46,
          70,
          81,
          89,
          95,
          101,
          106,
          111,
          116,
          121,
          126,
          131,
          137,
          144,
          153,
          160,
          165,
          168,
          170,
      ]
      t_p50 = [
          50,
          75,
          87,
          95,
          103,
          109,
          115,
          121,
          127,
          133,
          138,
          144,
          149,
          156,
          164,
          170,
          174,
          176,
          177,
      ]
      t_p97 = [
          54,
          80,
          93,
          102,
          110,
          117,
          124,
          130,
          137,
          144,
          151,
          157,
          162,
          169,
          176,
          181,
          184,
          186,
          187,
      ]
      p_p3 = [
          2.5,
          8.5,
          10.5,
          12.0,
          13.5,
          15.0,
          16.5,
          18.5,
          21.0,
          23.5,
          26.5,
          30.0,
          34.0,
          38.5,
          44.0,
          49.0,
          53.0,
          56.0,
          58.0,
      ]
      p_p50 = [
          3.3,
          10.2,
          12.5,
          14.5,
          16.5,
          18.5,
          20.5,
          23.0,
          25.5,
          29.0,
          32.5,
          37.0,
          41.5,
          47.0,
          53.5,
          59.0,
          63.0,
          66.0,
          68.0,
      ]
      p_p97 = [
          4.2,
          12.0,
          14.8,
          17.2,
          19.5,
          22.0,
          25.0,
          28.5,
          32.0,
          36.5,
          41.5,
          47.5,
          54.0,
          61.5,
          69.0,
          75.0,
          79.0,
          82.0,
          84.0,
      ]
      imc_p3 = [
          13.0,
          14.5,
          14.2,
          13.8,
          13.5,
          13.5,
          13.6,
          13.8,
          14.2,
          14.6,
          15.2,
          15.8,
          16.5,
          17.2,
          18.0,
          18.6,
          19.2,
          19.7,
          20.0,
      ]
      imc_p50 = [
          16.8,
          16.5,
          15.8,
          15.3,
          15.2,
          15.3,
          15.5,
          15.8,
          16.3,
          16.9,
          17.6,
          18.4,
          19.3,
          20.2,
          21.0,
          21.8,
          22.4,
          22.9,
          23.3,
      ]
      imc_p97 = [
          20.0,
          19.2,
          18.0,
          17.5,
          17.6,
          18.0,
          18.6,
          19.5,
          20.6,
          21.8,
          23.0,
          24.3,
          25.5,
          26.8,
          27.9,
          28.8,
          29.5,
          30.0,
          30.5,
      ]
    else:
      t_p3 = [
          45,
          68,
          80,
          88,
          94,
          100,
          105,
          110,
          115,
          120,
          125,
          131,
          138,
          145,
          150,
          153,
          155,
          156,
          157,
      ]
      t_p50 = [
          49,
          74,
          86,
          94,
          102,
          108,
          114,
          120,
          126,
          132,
          138,
          144,
          151,
          157,
          161,
          163,
          164,
          165,
          165,
      ]
      t_p97 = [
          53,
          79,
          92,
          101,
          109,
          116,
          123,
          130,
          137,
          144,
          151,
          158,
          164,
          169,
          172,
          174,
          175,
          175,
          176,
      ]
      p_p3 = [
          2.4,
          7.9,
          9.8,
          11.5,
          13.0,
          14.5,
          16.0,
          18.0,
          20.5,
          23.0,
          26.0,
          30.0,
          35.0,
          40.0,
          45.0,
          48.0,
          50.0,
          51.0,
          52.0,
      ]
      p_p50 = [
          3.2,
          9.5,
          11.8,
          13.8,
          15.8,
          17.8,
          19.8,
          22.2,
          25.0,
          28.5,
          32.5,
          37.5,
          43.0,
          48.5,
          53.5,
          57.0,
          59.0,
          60.0,
          61.0,
      ]
      p_p97 = [
          4.0,
          11.2,
          14.0,
          16.5,
          19.0,
          21.5,
          24.5,
          28.0,
          32.0,
          37.0,
          43.0,
          49.5,
          57.0,
          63.5,
          69.0,
          72.0,
          74.0,
          75.0,
          76.0,
      ]
      imc_p3 = [
          12.8,
          14.0,
          13.8,
          13.5,
          13.2,
          13.1,
          13.2,
          13.4,
          13.7,
          14.2,
          14.8,
          15.5,
          16.2,
          17.0,
          17.8,
          18.4,
          18.8,
          19.2,
          19.5,
      ]
      imc_p50 = [
          16.5,
          16.0,
          15.4,
          15.0,
          14.9,
          15.0,
          15.2,
          15.6,
          16.1,
          16.8,
          17.6,
          18.5,
          19.5,
          20.5,
          21.4,
          22.1,
          22.6,
          23.0,
          23.2,
      ]
      imc_p97 = [
          19.8,
          18.8,
          17.6,
          17.2,
          17.4,
          17.8,
          18.5,
          19.4,
          20.5,
          21.8,
          23.2,
          24.6,
          25.9,
          27.1,
          28.2,
          29.0,
          29.6,
          30.1,
          30.4,
      ]


    def creer_figure(y_p3, y_p50, y_p97, val_enfant, titre, y_label):
      fig, ax = plt.subplots(figsize=(6, 8))
      ax.set_xlim(0, 18)
      ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
      ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.2))
      ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))
      ax.grid(
          True, which="major", color="#e09f3e", linestyle="-", linewidth=0.7
      )
      ax.grid(
          True,
          which="minor",
          color="#f3d2a7",
          linestyle=":",
          linewidth=0.4,
      )
      ax.set_facecolor("#fff3e6")

      ax.plot(
          ages_ref,
          y_p97,
          color="#d35400",
          linestyle="--",
          linewidth=1.5,
          label="97e percentile",
      )
      ax.plot(
          ages_ref,
          y_p50,
          color="#27ae60",
          linewidth=2.5,
          label="50e percentile (Médiane)",
      )
      ax.plot(
          ages_ref,
          y_p3,
          color="#d35400",
          linestyle="--",
          linewidth=1.5,
          label="3e percentile",
      )
      ax.scatter(
          [age_ans],
          [val_enfant],
          color="#c0392b",
          s=120,
          zorder=5,
          label=f"Mesure ({val_enfant})",
      )

      ax.set_title(f"{titre} - {sexe}", fontsize=12, fontweight="bold")
      ax.set_xlabel("Âge (ans)", fontsize=10)
      ax.set_ylabel(y_label, fontsize=10)
      ax.legend(loc="upper left", fontsize=8)
      return fig


    # Affichage direct sur la page web mobile
    st.subheader("📊 Courbe de Taille")
    fig_t = creer_figure(t_p3, t_p50, t_p97, taille, "Taille", "cm")
    st.pyplot(fig_t)

    st.subheader("📊 Courbe de Poids")
    fig_p = creer_figure(p_p3, p_p50, p_p97, poids, "Poids", "kg")
    st.pyplot(fig_p)

    st.subheader("📊 Courbe d'IMC")
    fig_imc = creer_figure(imc_p3, imc_p50, imc_p97, imc, "IMC", "IMC")
    st.pyplot(fig_imc)

    # --- GÉNÉRATION DU PDF EN MÉMOIRE ---
    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=A4)

    # Sauvegarde temporaire des graphiques pour le PDF
    fig_t.savefig("t.png", dpi=150, facecolor=fig_t.get_facecolor())
    fig_p.savefig("p.png", dpi=150, facecolor=fig_p.get_facecolor())
    fig_imc.savefig("i.png", dpi=150, facecolor=fig_imc.get_facecolor())
    plt.close("all")

    pages = [
        ("Taille", "t.png", f"{taille} cm"),
        ("Poids", "p.png", f"{poids} kg"),
        ("IMC", "i.png", f"{imc} kg/m²"),
    ]

    for idx, (nom_m, img, val_s) in enumerate(pages):
      pdf.setFont("Helvetica-Bold", 16)
      pdf.drawString(50, 805, f"Bilan de Croissance - {nom_m}")
      pdf.setFont("Helvetica", 11)
      pdf.drawString(
          50,
          785,
          f"Nom : {nom} | Sexe : {sexe} | Naissance : {date_naiss_str} ({age_ans}"
          " ans)",
      )
      pdf.drawString(50, 770, f"Mesure actuelle : {val_s}")
      pdf.setLineWidth(1)
      pdf.setStrokeColorRGB(0.8, 0.8, 0.8)
      pdf.line(50, 760, 545, 760)

      pdf.drawImage(img, 40, 60, width=515, height=680)
      pdf.setFont("Helvetica-Oblique", 9)
      pdf.drawString(50, 30, f"Page {idx + 1} sur 3")

      if idx < len(pages) - 1:
        pdf.showPage()

    pdf.save()
    pdf_buffer.seek(0)

    # Bouton de téléchargement direct sur le téléphone
    st.download_button(
        label="📥 Télécharger le Bilan PDF Complet",
        data=pdf_buffer,
        file_name=f"Bilan_Croissance_{nom.replace(' ', '_')}.pdf",
        mime="application/pdf",
    )

  except Exception as e:
    st.error(
        f"Erreur dans les données saisies (Format date requis : JJ/MM/AAAA)."
        f" Détail : {e}"
    )