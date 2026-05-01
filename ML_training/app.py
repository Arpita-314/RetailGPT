import streamlit as st
import torch
import matplotlib.pyplot as plt
from xray_toolkit import generate_aperture, simulate_diffraction, tv_regularized_reconstruction

st.title("X-ray Imaging Toolkit")

st.sidebar.title("Parameters")
shape = st.sidebar.selectbox("Aperture Shape", ["circle", "rectangle", "slit"])
size = st.sidebar.slider("Aperture Size", 128, 512, 256)
iterations = st.sidebar.slider("Iterations", 10, 100, 50)

if st.button("Run Diffraction"):
    aperture = generate_aperture(shape, size)
    diffraction_pattern = simulate_diffraction(aperture)

    st.subheader("Aperture")
    st.image(aperture.numpy(), caption="Aperture", use_column_width=True)

    st.subheader("Diffraction Pattern")
    st.image(torch.log(1 + diffraction_pattern).numpy(), caption="Diffraction Pattern", use_column_width=True)

