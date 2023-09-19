
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

# Coloured noise generation code modified from https://stackoverflow.com/questions/67085963/generate-colors-of-noise-in-python
def noise_psd(N, psd = lambda f: 1.):
        X_white = np.fft.rfft(np.random.randn(N))
        S = psd(np.fft.rfftfreq(N))
        S = S / np.sqrt(np.mean(S**2.))
        X_shaped = X_white * S
        return np.fft.irfft(X_shaped)

def PSDGenerator(f):
    return lambda N: noise_psd(N, f)

@PSDGenerator
def coloured_noise(f):
    global noise_exponent
    return 1./np.where(f==0., float('inf'), f**noise_exponent)

st.set_page_config(layout='wide')
st.title('Stacked noisy sines')

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
    dataset_duration_days = st.number_input(label='Dataset duration (days):',
                                            value=90,
                                            min_value=1,
                                            max_value=2880,
                                            step=90)
    
    sample_rate_minutes = st.number_input(label='Sample rate (minutes):',
                                          value=60,
                                          min_value=1,
                                          max_value=360,
                                          step=1)
        
    noise_exponent = st.number_input(label='Noise exponent value:',
                                     value=1.,
                                     min_value=-10.0,
                                     max_value=10.,
                                     step=1.)
    
    noise_level = st.number_input(label='Noise level:',
                                  value=0,
                                  min_value=0,
                                  max_value=100,
                                  step=1)
    
    number_stacks = st.number_input(label='Number of stacks:',
                                    value=2,
                                    min_value=1,
                                    max_value=10,
                                    step=1)

    plot_type = st.selectbox(label='Plot type:',
                             options=['Linear', 'Log-Log'])


    pi = np.pi
    DT = sample_rate_minutes/60./24. # Convert to days
    Fs = 1./DT
    T = dataset_duration_days*number_stacks
    F1, F2, F3, F4, F5 = 0.9, 1.0, 1.8, 1.9, 2.0 # in cpd
    W1, W2, W3, W4, W5 = 2.*pi*F1, 2.*pi*F2, 2.*pi*F3, 2.*pi*F4, 2.*pi*F5
    t = np.arange(0., T, DT)
        
    Ft = (np.sin(W1*t) +np.sin(W2*t) +np.sin(W3*t) +np.sin(W4*t) +np.sin(W5*t) +
          coloured_noise(len(t)))
    F0, A0, P0 = DFT(Ft, Fs)
    
    Ft_stacked = np.mean(np.reshape(Ft, [len(Ft)//number_stacks, number_stacks]), 
                         axis=1)
    F1, A1, P1 = DFT(Ft_stacked, Fs/number_stacks)

with c2:
    fig, ax = plt.subplots(3, 1, figsize=[16.00/2.54, 10.00/2.54])
    ax[0].plot(t/30., Ft)
    ax[0].set_xlabel('Time (months)')
    ax[0].set_ylabel('Magnitude')
    ax[0].grid(True, which='both', c='Gainsboro')

    if plot_type=='Linear':
        ax[1].plot(F0, A0, c='Pink')
        ax[1].plot(F1, A1, c=u'#1f77b4')
        ax[1].set_xlim(0.5, 2.5)
    elif plot_type=='Log-Log':
        ax[1].loglog(F0, A0, c='silver')
        ax[1].loglog(F1, A1, c=u'#1f77b4')
    ax[1].set_xlabel('Frequency (cycles per day)')
    ax[1].set_ylabel('Amplitude')
    ax[1].grid(True, which='both', c='Gainsboro')
    ax[1].set_ylim(-0.05, 1.05)
    
    ax[2].plot(F0, P0, c='Pink')
    ax[2].plot(F1, P1, c=u'#1f77b4')
    ax[2].set_xlim(0.5, 2.5)
    ax[2].set_xlabel('Frequency (cycles per day)')
    ax[2].set_ylabel('Phase (radians)')
    ax[2].grid(True, which='both', c='Gainsboro')
    ax[2].set_yticks([-pi, 0., pi])
    ax[2].set_yticklabels([r'$-\pi$', '0', r'$+\pi$'])
    ax[2].set_ylim(-pi, pi)
    
    plt.tight_layout()    
    st.pyplot(fig)
