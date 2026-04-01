def make_pos_from_names(ch_names, montage_name='standard_1020'):
    import mne
    import numpy as np
    montage = mne.channels.make_standard_montage(montage_name)
    pos_dict = montage.get_positions()['ch_pos']
    # select channels in the order of ch_names
    pos = np.array([pos_dict[name][:2] for name in ch_names])
    return pos

def plot_spatial_filters(w, ch_names, cmap_name='autumn'):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import colormaps
    from matplotlib.colors import Normalize
    import mne

    w = np.asarray(w)
    pos = make_pos_from_names(ch_names)  # (n_channels, 2)

    norm = Normalize(vmin=np.min(w), vmax=np.max(w))
    cmap = colormaps.get_cmap(cmap_name)

    fig, ax = plt.subplots()
    mne.viz.plot_topomap(
        np.zeros(len(w)),
        pos,
        axes=ax,
        cmap=cmap_name,
        show=False,
        outlines='head',
        contours=0,
        sensors=False,
    )

    for weight, (x, y) in zip(w, pos):
        color = cmap(norm(weight))
        ax.plot(x, y, marker='o', markersize=8,
                markerfacecolor=color, markeredgecolor='k', linewidth=1)

    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label='Spatial filter weight')
    plt.show()