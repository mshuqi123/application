#!/usr/bin/python
# -*- coding: UTF-8 -*-

from configs import Basic_output


def Unit_conversion(data):
    """单位换算"""
    final = 0
    unit = "个"
    if isinstance(data, int) or isinstance(data, float):
        final_data = int(data)
        get_c = len(str(final_data)) // 4
        final = data / (1000 ** get_c)
        if len(str(int(final))) >= 4:
            final = final / 1000
            unit = Basic_output.dw[get_c + 1]
        else:
            unit = Basic_output.dw[get_c]
        return final, unit
    if isinstance(data, tuple):
        index = Basic_output.dw.index(data[1])
        final_data = int(data[0])
        # print(final_data)
        get_c = len(str(final_data)) // 4
        final = data[0] / (1000 ** get_c)
        if len(str(int(final))) >= 4:
            final = final / 1000
            unit = Basic_output.dw[index + get_c + 1]
        else:
            unit = Basic_output.dw[index + get_c]

    return round(final, 6), unit

def get_sum(data):
    """汇总计算"""
    dw = []
    if len(data) == 1:
        return data[0]
    for i in data:
        dw.append(i[1])
    xdw = set(dw)
    if len(xdw) == 1:
        sall = []
        for z in data:
            sall.append(z[0])
        all = (sum(sall), dw[0])
        return Unit_conversion(all)
    else:
        sdw = []
        for s in xdw:
            sdw.append(Basic_output.dw.index(s))
        sdw.sort()
        mdw = max(sdw)
        xall = []
        for z in data:
            if (mdw - Basic_output.dw.index(z[1])) == 0:
                xall.append(z[0])
            else:
                xd = z[0] / (1000 ** (mdw - Basic_output.dw.index(z[1])))
                xall.append(xd)
        s = (sum(xall), Basic_output.dw[mdw])
        return Unit_conversion(s)

def get_sum2(data):
    """汇总计算"""
    all = data[0: 2]
    xall = get_sum(all)
    for i in data[2:]:
        if i[0] == 0.0 or i[0] == 0:
            continue
        else:
            if xall[1] == i[1]:
                xall = Unit_conversion(((xall[0] + i[0]), xall[1]))
            else:
                ldw = Basic_output.dw.index(xall[1])
                xdw = Basic_output.dw.index(i[1])
                if ldw > xdw:
                    xd = i[0] / (1000 ** (ldw - xdw))
                    xall = Unit_conversion(((xall[0] + xd), xall[1]))
                else:
                    xd = xall[0] / (1000 ** (xdw - ldw))
                    xall = Unit_conversion(((i[0] + xd), i[1]))

    return xall


if __name__ == '__main__':
    u = Unit_conversion(7010000000.0)
    # u = Unit_conversion((7010000, 'aa'))
    # print(u)
    d = [(323008.21366779803, '个'), (361769.19930793386, '个'), (405181.50322488596, '个'), (453803.28361187235, '个'), (508259.6776452971, '个'), (569250.8389627327, '个'), (637560.9396382608, '个'), (714068.252394852, '个'), (799756.4426822345, '个'), (895727.2158041026, '个'), (1003214.481700595, '个'), (1123600.2195046665, '个'), (1258432.2458452268, '个'), (1409444.1153466539, '个'), (1578577.4091882526, '个'), (1768006.698290843, '个'), (1980167.5020857444, '个'), (2217787.602336034, '个'), (2483922.1146163587, '个'), (2781992.7683703215, '个'), (3115831.9005747605, '个'), (3489731.7286437326, '个'), (3908499.53608098, '个'), (4377519.480410699, '个'), (4902821.818059983, '个'), (5491160.436227181, '个'), (6150099.688574444, '个'), (6888111.651203376, '个'), (7714685.049347783, '个'), (8640447.255269518, '个'), (9677300.92590186, '个'), (10838577.037010087, '个'), (12139206.281451298, '个'), (13595911.035225455, '个'), (15227420.359452512, '个'), (17054710.802586813, '个'), (19101276.09889723, '个'), (21393429.230764903, '个'), (23960640.738456693, '个'), (26835917.6270715, '个'), (30056227.74232008, '个'), (33662975.07139849, '个'), (37702532.07996632, '个'), (42226835.92956228, '个'), (47294056.24110975, '个'), (52969342.99004293, '个'), (59325664.14884809, '个'), (66444743.84670986, '个'), (74418113.10831505, '个'), (83348286.68131287, '个')]
    z = get_sum2(d)
    print(z)