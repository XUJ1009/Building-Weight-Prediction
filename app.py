import streamlit as st
import numpy as np

st.write("<h1 style='text-align:center'>Building Weight Calculator", unsafe_allow_html=True)

structures = ['F-CW', 'F-SW', 'SW', 'F']
col1, col2 = st.columns(2)

with col1:
    H = st.number_input("H (m)", min_value=0.00)
    N = st.number_input("N", min_value=0.00)
    L = st.number_input("L (m)", min_value=0.00)
    b = st.selectbox('LFRS', structures)
with col2:
    B = st.number_input("B (m)", min_value=0.00)
    S = st.number_input("S (m$^2$)", min_value=0.00)
    T = st.number_input("T (s)", min_value=0.00)

# text = 'init'
def calc_M():

    if any(x < 0 for x in [H, N, L, B, S, T]):
        return "Input values must be non-negative"

    if any(x == 0 for x in [N, L, B]) and b != structures[0]:
        return "Insufficient input parameters"

    # chose correct eq from 4*4*3=48 (4 LFRS, 4 Cond, 3 equations)
    s11, s11u, s11d = lambda s: 16.737*s, lambda s: 16.765*s+562951, lambda s: 16.710*s-562951
    s21, s21u, s21d = lambda s: 18.004*s, lambda s: 18.076*s+282748, lambda s: 17.932*s-282748
    s31, s31u, s31d = lambda s: 18.724*s, lambda s: 18.781*s+109660, lambda s: 18.667*s-109660,
    s41, s41u, s41d = lambda s: 15.181*s, lambda s: 15.276*s+90048 , lambda s: 15.087*s-90048

    s12, s12u, s12d = lambda l,b,n:1.062*np.log10(n)+0.506*np.log10(l*b)+2.750, lambda l,b,n:1.058*np.log10(n)+0.498*np.log10(l*b)+2.933, lambda l,b,n:1.058*np.log10(n)+0.498*np.log10(l*b)+2.566
    s22, s22u, s22d = lambda l,b,n:0.932*np.log10(n)+0.783*np.log10(l*b)+2.010, lambda l,b,n:0.934*np.log10(n)+0.785*np.log10(l*b)+2.235, lambda l,b,n:0.930*np.log10(n)+0.782*np.log10(l*b)+1.787
    s32, s32u, s32d = lambda l,b,n:1.050*np.log10(n)+0.907*np.log10(l*b)+1.380, lambda l,b,n:1.050*np.log10(n)+0.907*np.log10(l*b)+1.498, lambda l,b,n:1.050*np.log10(n)+0.907*np.log10(l*b)+1.261
    s42, s42u, s42d = lambda l,b,n:1.019*np.log10(n)+0.960*np.log10(l*b)+1.231, lambda l,b,n:1.019*np.log10(n)+0.960*np.log10(l*b)+1.367, lambda l,b,n:1.019*np.log10(n)+0.960*np.log10(l*b)+1.094

    s13, s13u, s13d = lambda l,h,n,t:0.697*np.log10(h)+0.610*np.log10(l)+0.552*np.log10(n)-0.144*np.log10(t)+2.727, lambda l,h,n,t:0.696*np.log10(h)+0.609*np.log10(l)+0.551*np.log10(n)-0.144*np.log10(t)+2.933, lambda l,h,n,t:0.698*np.log10(h)+0.611*np.log10(l)+0.553*np.log10(n)-0.144*np.log10(t)+2.521
    s23, s23u, s23d = lambda l,h,n,t:1.192*np.log10(h)+1.233*np.log10(l)-0.189*np.log10(n)+0.0699*np.log10(t)+1.519, lambda l,h,n,t:1.198*np.log10(h)+1.240*np.log10(l)-0.190*np.log10(n)+0.0703*np.log10(t)+1.789, lambda l,h,n,t:1.186*np.log10(h)+1.226*np.log10(l)-0.188*np.log10(n)+0.0695*np.log10(t)+1.249
    s33, s33u, s33d = lambda l,h,n,t:1.750*np.log10(h)+0.910*np.log10(l)-0.260*np.log10(n)-0.187*np.log10(t)+1.037, lambda l,h,n,t:1.749*np.log10(h)+0.909*np.log10(l)-0.260*np.log10(n)-0.187*np.log10(t)+1.198, lambda l,h,n,t:1.750*np.log10(h)+0.910*np.log10(l)-0.260*np.log10(n)-0.187*np.log10(t)+0.879
    s43, s43u, s43d = lambda l,h,n,t:1.198*np.log10(h)+1.305*np.log10(l)+0.301*np.log10(n)-0.0569*np.log10(t)+0.871, lambda l,h,n,t:1.198*np.log10(h)+1.305*np.log10(l)+0.301*np.log10(n)-0.0569*np.log10(t)+1.185, lambda l,h,n,t:1.198*np.log10(h)+1.305*np.log10(l)+0.301*np.log10(n)-0.0569*np.log10(t)+0.556

    s14, s14u, s14d = lambda h: 424.46*h**1.497 + 349454, lambda h: 212.701*h**1.606 + 1410179, lambda h: 490.129*h**1.473 - 671518
    s34, s34u, s34d = lambda h: 1.458*np.log10(h) + 2.628, lambda h: 1.458*np.log10(h) + 2.991, lambda h: 1.459*np.log10(h) + 2.265
    s44, s44u, s44d = lambda h: 2.390*np.log10(h) + 1.823, lambda h: 2.388*np.log10(h) + 2.457, lambda h: 2.392*np.log10(h) + 1.189,

    cond1 = L*H*N*T != 0 
    cond2 = L*B*N !=0 and H*T==0
    cond3 = H != 0 and L*B*N == 0
    cond4 = S!=0 and (H == 0 or L*B*N==0 or L*H*N*T==0)

    cond1 = S != 0
    cond2 = L*B*N != 0
    cond3 = L*H*N*T != 0
    cond4 = H != 0

    if b == structures[0]:
        if cond1:
            ans, upper, lower = s11(S), s11u(S), s11d(S)
            text = f'{b} (Eq. 1) : W = {ans:.0f} kN [{lower:.0f}, {upper:.0f}]kN'
        elif cond2:
            ans, upper, lower = np.power(10,s12(L,B,N)), np.power(10,s12u(L,B,N)), np.power(10,s12d(L,B,N))
            text = f'{b} (Eq. 2) : W = {ans:.3f} kN [{lower:.0f}, {upper:.0f}]kN'
        elif cond3:
            ans, upper, lower = np.power(10,s13(L,H,N,T)), np.power(10,s13u(L,H,N,T)), np.power(10,s13d(L,H,N,T))
            text = f'{b} (Eq. 3) : W = {ans:.3f} kN [{lower:.0f}, {upper:.0f}]kN'
        elif cond4:
            ans, upper, lower = s14(H), s14u(H), s14d(H)
            text = f'{b} (Eq. 4) : W = {ans:.3f} kN [{lower:.0f}, {upper:.0f}]kN'
        else:
            text = 'no applicable equation'
    elif b == structures[1]:
        if cond1:
            ans, upper, lower = s21(S), s21u(S), s21d(S)
            text = f'{b} (Eq. 1) : W = {ans:.0f} kN [{lower:.0f}, {upper:.0f}]kN'
        elif cond2:
            ans, upper, lower = np.power(10,s22(L,B,N)), np.power(10,s22u(L,B,N)), np.power(10,s22d(L,B,N))
            text = f'{b} (Eq. 2) : W = {ans:.3f} kN [{lower:.0f}, {upper:.0f}]kN'
        elif cond3:
            ans, upper, lower = np.power(10,s23(L,H,N,T)), np.power(10,s23u(L,H,N,T)), np.power(10,s23d(L,H,N,T))
            text = f'{b} (Eq. 3) : W = {ans:.3f} kN [{lower:.0f}, {upper:.0f}]kN'
        else:
            text = 'no applicable equation'
    elif b == structures[2]:
        if cond1:
            ans, upper, lower = s31(S), s31u(S), s31d(S)
            text = f'{b} (Eq. 1) : W = {ans:.0f} kN [{lower:.0f}, {upper:.0f}]kN'
        elif cond2:
            ans, upper, lower = np.power(10,s32(L,B,N)), np.power(10,s32u(L,B,N)), np.power(10,s32d(L,B,N))
            text = f'{b} (Eq. 2) : W = {ans:.3f} kN [{lower:.0f}, {upper:.0f}]kN'
        elif cond3:
            ans, upper, lower = np.power(10,s33(L,H,N,T)), np.power(10,s33u(L,H,N,T)), np.power(10,s33d(L,H,N,T))
            text = f'{b} (Eq. 3) : W = {ans:.3f} kN [{lower:.0f}, {upper:.0f}]kN'
        elif cond4:
            ans, upper, lower = np.power(10,s34(H)), np.power(10,s34u(H)), np.power(10,s34d(H))
            text = f'{b} (Eq. 4) : W = {ans:.3f} kN [{lower:.0f}, {upper:.0f}]kN'
        else:
            text = 'no applicable equation'
    elif b == structures[3]:
        if cond1:
            ans, upper, lower = s41(S), s41u(S), s41d(S)
            text = f'{b} (Eq. 1) : W = {ans:.0f} kN [{lower:.0f}, {upper:.0f}]kN'
        elif cond2:
            ans, upper, lower = np.power(10,s42(L,B,N)), np.power(10,s42u(L,B,N)), np.power(10,s42d(L,B,N))
            text = f'{b} (Eq. 2) : W = {ans:.3f} kN [{lower:.0f}, {upper:.0f}]kN'
        elif cond3:
            ans, upper, lower = np.power(10,s43(L,H,N,T)), np.power(10,s43u(L,H,N,T)), np.power(10,s43d(L,H,N,T))
            text = f'{b} (Eq. 3) : W = {ans:.3f} kN [{lower:.0f}, {upper:.0f}]kN'
        elif cond4:
            ans, upper, lower = np.power(10,s44(H)), np.power(10,s44u(H)), np.power(10,s44d(H))
            text = f'{b} (Eq. 4) : W = {ans:.3f} kN [{lower:.0f}, {upper:.0f}]kN'
        else:
            text = 'no applicable equation'
    return text

solve = st.button("Calculate")
if solve:
    text = calc_M()
    st.write(text)


st.write('---')

st.write("""
|LFRS |$S/m^2$ <br/> (1) | $L/m, B/m, N$  <br/> (2)               | $L/m, H/m, N, T/s$    <br/> (3)                           | $H/m$  <br/> (4)                |
|-----|--------------    |------------------------                |-------------------------------------                      |---------------------------------|
|F-CW | $W = 16.737S$    | $lgW = 1.062lgN + 0.506lg(LB) + 2.750$ | $lgW = 0.697lgH + 0.610lgL + 0.552lgN - 0.144lgT + 2.727$ | $W = 424.46H^{1.497} + 349454$ |
|F-SW | $W = 18.004S$    | $lgW = 0.932lgN + 0.783lg(LB) + 2.010$ | $lgW = 1.192lgH + 1.233lgL - 0.189lgN + 0.0699lgT + 1.519$ |        --                       |
|SW   | $W = 18.724S$    | $lgW = 1.050lgN + 0.907lg(LB) + 1.380$ | $lgW = 1.750lgH + 0.910lgL - 0.260lgN - 0.187lgT + 1.037$ | $lgW = 1.458lgH + 2.628$        |
|F    | $W = 15.181S$    | $lgW = 1.019lgN + 0.960lg(LB) + 1.231$ | $lgW = 1.198lgH + 1.305lgL + 0.301lgN - 0.0569lgT + 0.871$ | $lgW = 2.390lgH + 1.823$        | 
""", unsafe_allow_html=True)
