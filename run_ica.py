# Author: Nicolas Legrand (legrand@cyceron.fr)

import matplotlib.pyplot as plt
import mne
from mne.preprocessing import ICA
import numpy as np
import os

root = 'D:/'
Names = os.listdir(root + 'EEG/')  # Subjects ID


def run_ICA(subject):
    """Filter raw data.

    Parameters
    ----------
    *subject: string
        The participant reference

    Save the resulting *-raw.fif file in the '2_rawfilter' directory.

    """
    input_path = root + '/3_epochs/' + subject + 'clean-epo.fif'
    epochs = mne.read_epochs(input_path)

    # ICA correction
    ica = ICA(n_components=0.95, method='fastica')

    picks = mne.pick_types(epochs.info, meg=False, eeg=True, eog=False,
                           stim=False, exclude='bads')

    ica.fit(epochs, picks=picks, decim=10)

#    ica.plot_components()
#    ica.plot_scores(scores)
#    eog_inds = ica.exclude

    # List of bad component to reject
    eog_inds = []

    fig, axs = plt.subplots(2, 2, figsize=(14, 6))
    axs = axs.ravel()

    for i, eo in enumerate(['E8', 'E14', 'E21', 'E25']):
        inds, scores = ica.find_bads_eog(epochs, ch_name=eo)
        axs[i].set_title(eo)
        axs[i].bar(np.arange(0, len(scores)), height=scores)
        axs[i].set_ylim([-0.7, 0.7])
        axs[i].axhline(y=-0.5, linestyle='--', color='r')
        axs[i].axhline(y=0.5, linestyle='--', color='r')

#        for i in inds:
#            if not i in eog_inds:
#                eog_inds.append(i)
    plt.title('Rejected: ' + str(eog_inds))
    plt.savefig(root + '/4_ICA/' + subject + '-scores.png')
    plt.clf()
    plt.close()

    # Plot components
    ica_plot = ica.plot_components(show=False)
    for i, plot in enumerate(ica_plot):
        plot
        plt.savefig(root + '/4_ICA/' + subject + str(i) + '-ica.png')
        plt.clf()
        plt.close()

    # Apply ICA
    ica.exclude = eog_inds
    ica.apply(epochs)

    # Save epochs
    epochs.save(root + '/4_ICA/' + subject + '-epo.fif')


# Loop across subjects
if __name__ == '__main__':

    for subject in Names:
        run_ICA(subject)
