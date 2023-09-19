
import streamlit as st
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


fontsize = 8
mpl.rcParams.update(mpl.rcParamsDefault)
mpl.rcParams[ 'font.sans-serif'  ] = 'Calibri'
mpl.rcParams[ 'font.size'        ] = fontsize
mpl.rcParams[ 'xtick.direction'  ] = 'out'
mpl.rcParams[ 'ytick.direction'  ] = 'out'       
mpl.rcParams[ 'lines.linewidth'  ] = 1.0     


def DFT(data, Fs):
    n = len(data)
    k = np.arange(n)
    F = (Fs*k/n)[:n//2]
    Z = (np.fft.fft(data)/(n//2))[:n//2]
    A = np.abs(Z)
    P = np.angle(Z)
    return F, A, P

st.set_page_config(layout='wide')
st.title('Stacked sines')

# Remove whitespace above app title
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

c1, c2 = st.columns([1,3])

with c1:
    test_duration_minutes = st.number_input(label='Test duration (minutes):',
                                            value=60,
                                            min_value=60,
                                            max_value=2880,
                                            step=30)
    
    sample_rate_seconds = st.number_input(label='Sample rate (seconds):',
                                          value=1,
                                          min_value=1,
                                          max_value=60,
                                          step=1)
    
    period_1_minutes = st.number_input(label='Period 1 (minutes):',
                                       value=1,
                                       min_value=1,
                                       max_value=60,
                                       step=1)
    
    period_2_minutes = st.number_input(label='Period 2 (minutes):',
                                       value=5,
                                       min_value=1,
                                       max_value=60,
                                       step=1)
    
    period_3_minutes = st.number_input(label='Period 3 (minutes):',
                                       value=10,
                                       min_value=1,
                                       max_value=60,
                                       step=1)
    
pi = np.pi
DT = sample_rate_seconds/60.
Fs = 1./DT
T = test_duration_minutes
P1, P2, P3 = period_1_minutes, period_2_minutes, period_3_minutes
F1, F2, F3 = 1./P1, 1./P2, 1./P3
W1, W2, W3 = 2.*pi*F1, 2.*pi*F2, 2.*pi*F3
t = np.arange(0., T+DT, DT)
Ft = np.sin(W1*t) + np.sin(W2*t) + np.sin(W3*t)
F, A, P = DFT(Ft, Fs)

with c2:
    fig, ax = plt.subplots(3, 1, figsize=[16.00/2.54, 10.00/2.54])
    ax[0].plot(t, Ft)
    ax[0].set_xlabel('Time (minutes)')
    ax[0].set_ylabel('Magnitude')
    ax[0].grid(True, which='both', c='Gainsboro')

    ax[1].semilogx(1./F, A)
    ax[1].set_xlabel('Period (minutes per cycle)')
    ax[1].set_ylabel('Amplitude')
    ax[1].grid(True, which='both', c='Gainsboro')
    ax[1].set_xlim(1e-1, 1e2)
    
    ax[2].semilogx(1./F, P)
    ax[2].set_xlabel('Period (minutes per cycle)')
    ax[2].set_ylabel('Phase (radians)')
    ax[2].grid(True, which='both', c='Gainsboro')
    ax[2].set_yticks([-pi, 0., pi])
    ax[2].set_yticklabels([r'$-\pi$', '0', r'$+\pi$'])
    ax[2].set_xlim(1e-1, 1e2)
    ax[2].set_ylim(-pi, pi)
    
    plt.tight_layout()
    st.pyplot(fig)
