import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(13)
m = np.array([0.04, 0.07, 0.11])
s = np.array([0.06, 0.18, 0.25])
corr = [[1, 0, 0], [0, 1, .5], [0, .5, 1]]
C = np.array(corr) * np.outer(s,s)
w = rng.dirichlet([1, 1, 1], 5000)
r = w @ m
v = np.sqrt((w @ C * w).sum(1))
o = np.argsort(v)
top = np.maximum.accumulate(r[o])
edge = o[r[o] >= top]
print(len(edge), 'of', len(w), 'mixes on the edge')
t, b = edge[0], edge[v[edge]<= s[1]][-1]
print(f'lowest risk: {v[t]:.1%}, return  {r[t]:.1%}')
print(f'edge at B`s risk {r[b]:.1%}, B {m[1]:.1%}')

#plot implementation
plt.figure(figsize=(12, 7))

sc = plt.scatter(v, r, c=r/v, cmap='viridis', s=12, alpha=0.4, label='Random Portfolios')
cbar = plt.colorbar(sc)
cbar.set_label('Return-to-Risk Ratio')


plt.plot(v[edge], r[edge], color='crimson', linewidth=3, label='Efficient Frontier')

asset_labels = ['Asset A', 'Asset B', 'Asset C']
plt.scatter(s, m, color='black', marker='X', s=120, zorder=5, label='Individual Assets')
for i, txt in enumerate(asset_labels):
    plt.annotate(f'{txt}\n(Risk: {s[i]:.1%}, Ret: {m[i]:.1%})',
                 (s[i], m[i]), textcoords="offset points", xytext=(12,-5), ha='left', fontsize=9, fontweight='semibold')


plt.scatter(v[t], r[t], color='blue', s=150, zorder=6, marker='o', edgecolors='white', label=f'Min Risk Portfolio ({v[t]:.1%})')
plt.scatter(v[b], r[b], color='purple', s=150, zorder=6, marker='s', edgecolors='white', label=f'Asset B Risk Level ({r[b]:.1%})')

plt.title('Markowitz Efficient Frontier & Portfolio Optimization', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Portfolio Risk / Volatility (Standard Deviation)', fontsize=11)
plt.ylabel('Expected Return', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)

plt.tight_layout()
plt.show()