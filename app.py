from datetime import datetime
import io
import os
import tempfile
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit as st

st.set_page_config(
    page_title="Suivi de Croissance 0-18 ans", page_icon="📈", layout="centered"
)

st.title("📈 Suivi de Croissance (0 - 18 ans)")
st.write(
    "Application de suivi global de la croissance de l'enfant (taille, poids,"
    " IMC)."
)

with st.form("form_saisie"):
  st.subheader("Informations de l'enfant")
  nom = st.text_input("Nom ou prénom de l'enfant", "Mon Enfant")
  sexe = st.selectbox("Sexe", ["Garçon", "Fille"])
  date_naiss_str = st.text_input("Date de naissance (JJ/MM/AAAA)", "15/06/2015")

  col1, col2 = st.columns(2)
  with col1:
    poids = st.number_input("Poids actuel (kg)", value=25.0, step=0.5)
  with col2:
    taille = st.number_input("Taille actuelle (cm)", value=120.0, step=1.0)

  btn_valider = st.form_submit_button("Générer le suivi 0-18 ans")

if btn_valider:
  try:
    date_naiss = datetime.strptime(date_naiss_str, "%d/%m/%Y")
    age_jours = (datetime.now() - date_naiss).days
    age_ans = round(age_jours / 365.25, 1)  # Âge en années
    taille_m = taille / 100.0
    imc = round(poids / (taille_m**2), 2)

    st.info(
        f"**{nom}** ({sexe}) — Âge : {age_ans} ans | Taille : {taille} cm |"
        f" Poids : {poids} kg | IMC : {imc}"
    )

    # Références de 0 à 18 ans (19 points)
    ages_ref = np.linspace(0, 18, 19)

    if sexe == "Garçon":
      t_p3 = np.linspace(46, 160, 19)
      t_p50 = np.linspace(50, 175, 19)
      t_p97 = np.linspace(54, 190, 19)
      p_p3 = np.linspace(2.5, 50, 19)
      p_p50 = np.linspace(3.3, 70, 19)
      p_p97 = np.linspace(4.2, 95, 19)
      imc_p3 = np.linspace(13.0, 16.0, 19)
      imc_p50 = np.linspace(16.5, 20.0, 19)
      imc_p97 = np.linspace(20.0, 26.0, 19)
    else:
      t_p3 = np.linspace(45, 150, 19)
      t_p50 = np.linspace(49, 163, 19)
      t_p97 = np.linspace(53, 178, 19)
      p_p3 = np.linspace(2.4, 45, 19)
      p_p50 = np.linspace(3.2, 60, 19)
      p_p97 = np.linspace(4.0, 85, 19)
      imc_p3 = np.linspace(12.8, 15.5, 19)
      imc_p50 = np.linspace(16.2, 19.5, 19)
      imc_p97 = np.linspace(19.8, 25.5, 19)


    def creer_figure(y_p3, y_p50, y_p97, val_enfant, titre, y_label):
      fig, ax = plt.subplots(figsize=(6, 8))
      ax.set_xlim(0, 18)
      ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
      ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
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

      # Point fin et élégant (s=40)
      ax.scatter(
    [age_ans],  # (ou age_mois pour le 0-3 ans)
    [val_enfant],
    color="#c0392b",
    marker="x",  # Vous pouvez tester 'x' ou '+'
    s=60,  # Taille de la croix (un peu plus grand qu'un rond pour bien la voir)
    zorder=5,
    label=f"Mesure ({val_enfant})",
)

      ax.set_title(f"{titre} (0-18 ans) - {sexe}", fontsize=12, fontweight="bold")
      ax.set_xlabel("Âge (années)", fontsize=10)
      ax.set_ylabel(y_label, fontsize=10)
      ax.legend(loc="upper left", fontsize=8)
      return fig


    st.subheader("📊 Courbe de Taille")
    fig_t = creer_figure(t_p3, t_p50, t_p97, taille, "Taille", "cm")
    st.pyplot(fig_t)

    st.subheader("📊 Courbe de Poids")
    fig_p = creer_figure(p_p3, p_p50, p_p97, poids, "Poids", "kg")
    st.pyplot(fig_p)

    st.subheader("📊 Courbe d'IMC")
    fig_imc = creer_figure(imc_p3, imc_p50, imc_p97, imc, "IMC", "kg/m²")
    st.pyplot(fig_imc)

    # --- Génération PDF sécurisée via tempfile ---
    temp_dir = tempfile.gettempdir()
    img_t = os.path.join(temp_dir, "temp_taille_18.png")
    img_p = os.path.join(temp_dir, "temp_poids_18.png")
    img_imc = os.path.join(temp_dir, "temp_imc_18.png")

    fig_t.savefig(img_t, dpi=150, facecolor=fig_t.get_facecolor())
    fig_p.savefig(img_p, dpi=150, facecolor=fig_p.get_facecolor())
    fig_imc.savefig(img_imc, dpi=150, facecolor=fig_imc.get_facecolor())
    plt.close("all")

    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=A4)

    pages = [
        ("Taille", img_t, f"{taille} cm"),
        ("Poids", img_p, f"{poids} kg"),
        ("IMC", img_imc, f"{imc} kg/m²"),
    ]

    for idx, (nom_m, img, val_s) in enumerate(pages):
      pdf.setFont("Helvetica-Bold", 16)
      pdf.drawString(50, 805, f"Bilan de Croissance (0-18 ans) - {nom_m}")
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

    st.download_button(
        label="📥 Télécharger le Bilan 0-18 ans (PDF)",
        data=pdf_buffer,
        file_name=f"Bilan_0_18ans_{nom.replace(' ', '_')}.pdf",
        mime="application/pdf",
    )

  except Exception as e:
    st.error(
        "Veuillez vérifier les saisies (Format date requis : JJ/MM/AAAA). Erreur"
        f" : {e}"
    )
