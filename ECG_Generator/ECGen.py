from math import sin, pi, cos



ecg_signal = []


def p_wav(x, a_pwav, d_pwav, t_pwav, li):

        l = li
        a = a_pwav
        x = x/100 + t_pwav
        b = (2 * l)/d_pwav
        n = 100
        p1 = 1 / l
        p2 = 0


        for i in range(1,101):
            harm1 = ((((sin((pi / (2 * b)) * (b - (2 * i)))) / (b - (2 * i)) + (sin((pi / (2 * b)) * (b + (
                2 * i)))) / (b + (2 * i))) * (2 / pi)) * cos((i * pi * x) / l))

            p2 = p2 + (harm1)

        p2 = (p2 + p1) * a
        pwav = p2


        return pwav

def q_wav(x, a_qwav, d_qwav, t_qwav, li):
        l = li
        x = x/100 + t_qwav
        a = a_qwav
        b = (2 * l) / d_qwav
        n = 100
        q1 = (a / (2 * b)) * (2 - b)
        q2 = 0

        for i in range(1,101):
            harm5 = (((2 * b * a) / (i * i * pi * pi)) * (1 - cos((i * pi) / b))) * cos((i * pi * x) / l)
            q2 = q2 + harm5


        q2 = (q2 + q1) * -1

        qwav = q2

        return qwav

def qrs_wav(x, a_qrswav, d_qrswav, li):

        l = li
        a = a_qrswav
        b = (2 * l) / d_qrswav
        n = 100
        qrs1 = (a / (2 * b)) * (2 - b)
        qrs2 = 0

        for i in range (1,101):
            harm = (((2 * b * a) / (i * i * pi * pi)) * (1 - cos((i * pi) / b))) * cos((i * pi * x/100) / l)
            qrs2 += harm



        qrs2 += qrs1

        qrswav = qrs2

        return qrswav

def s_wav(x, a_swav, d_swav, t_swav, li):
        l = li
        x = x/100 - t_swav
        a = a_swav
        b = (2 * l) / d_swav
        n = 100
        s1 = (a / (2 * b)) * (2 - b)
        s2 = 0

        for i in range (1,101):
            harm3 = (((2 * b * a) / (i * i * pi * pi)) * (1 - cos((i * pi) / b))) * cos((i * pi * x) / l)

            s2 += harm3


        s2 = (s2 + s1) * -1

        swav = s2
        return swav

def t_wav(x, a_twav, d_twav, t_twav, li):

        l = li
        a = a_twav
        x = x/100 - t_twav - 0.045
        b = (2 * l) / d_twav
        n = 100
        t1 = 1 / l
        t2 = 0

        for i in range (1,101):
            harm2 = (((sin((pi / (2 * b)) * (b - (2 * i)))) / (b - (2 * i)) + (sin(
                (pi / (2 * b)) * (b + (2 * i)))) / (b + (2 * i))) * (2 / pi)) * cos(
                (i * pi * x) / l)

            t2 += harm2


        t2 = (t2 + t1) * a

        #twav1 = t1 + t2
        twav = t2

        return twav

def u_wav(x, a_uwav, d_uwav, t_uwav, li):

        l = li
        a = a_uwav
        x = x/100 - t_uwav
        b = (2 * l) / d_uwav
        n = 100
        u1 = 1 / l
        u2 = 0

        for i in range (1,101):
            harm4 = (((sin((pi / (2 * b)) * (b - (2 * i)))) / (b - (2 * i)) + (sin((pi / (2 * b)) * (b + (
                2 * i)))) / (b + (2 * i))) * (2 / pi)) * cos((i * pi * x) / l)

            u2 += harm4


        u2 = (u2 + u1) * a


        uwav = u2


        return uwav

def ecg_gen_norm (rate):


        li = 30 / rate
        a_pwav = 0.25

        d_pwav = 0.09
        t_pwav = 0.16

        a_qwav = 0.025
        d_qwav = 0.066
        t_qwav = 0.166

        a_qrswav = 1.6
        d_qrswav = 0.11

        a_swav = 0.25
        d_swav = 0.066
        t_swav = 0.09

        a_twav = 0.35
        d_twav = 0.142
        t_twav = 0.2

        a_uwav = 0.035
        d_uwav = 0.0476
        t_uwav = 0.433

        for x in range(1,1000,1):
            pwav = p_wav(x, a_pwav, d_pwav, t_pwav, li)


            qwav = q_wav(x, a_qwav, d_qwav, t_qwav, li)

            qrswav = qrs_wav(x, a_qrswav, d_qrswav, li)

            swav = s_wav(x, a_swav, d_swav, t_swav, li)

            twav = t_wav(x, a_twav, d_twav, t_twav, li)


            uwav = u_wav(x, a_uwav, d_uwav, t_uwav, li)


            ecg_signal.append(pwav+qrswav+twav+swav+qwav+uwav)

        return ecg_signal




