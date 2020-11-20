import ismrmrd
import h5py

""" function to insert protocol into ismrmrd file

The protocol should be saved as an hdf5 file with groups 'hdr' and 'acquisitions'.
Protocol data, which contain a single number (e.g dwelltime) are stored as attributes,
protocol data, which contain arrays (e.g. acquisition data) are stored as datasets.

"""
# In Sequenzdatei hdf5-Datei erzeugen, die hdr und acquisitions enthält. Der header kann am Ende gesetzt werden, die Acquisition Parameter (auch Gradienten) müssen während der Sequenzerzeugung gesetzt werden.


# in bart_pulseq Funktion ohne for loop für Akquisitionen und statt dem gesamenten Protokoll nur die jeweilige Akquistion übergeben.
# Header nur beim ersten mal reinschreiben??
# ismrmrd durch metadata ersetzen.

def insert_prot(prot_file, ismrmrd_file): # später durch args ersetzen, um ein command line tool zu erstellen

    #---------------------------
    # Read protocol and Ismrmrd file
    #---------------------------

    prot = h5py.File(prot_file, 'r')
    dset = ismrmrd.Dataset(ismrmrd_file)

    #---------------------------
    # First process the header 
    #---------------------------

    prot_hdr = prot['hdr']
    dset_hdr = ismrmrd.xsd.CreateFromDocument(dset.read_xml_header())

    dset_hdr.encoding[0].encodedSpace.matrixSize.x = prot['hdr']['encoding']['0']['encodedSpace']['matrixSize'].attrs['x']


    # write header back to file
    dset.write_xml_header(dset_hdr.toxml())


    #---------------------------
    # Now process all acquisitions
    #---------------------------

    # first check if number of acquisitions is the same in both files
    if not len(prot['acquisitions']) == dset.number_of_acquisitions():
        raise ValueError('Number of acquisitions in protocol and Ismrmrd file is not the same.')

    for n, prot_acq in enumerate(prot['acquisitions']):

        dset_acq = dset.read_acquisition(n)

        dset_acq.idx.slice = prot_acq['idx'].attrs['slice']
        dset_acq.setFlag()
        dset_acq.data
        dset_acq.traj = calc_traj()

        dset.write_acquisition(dset_acq, n)

    dset.close()
    prot.close()

def calc_traj(grads, adc):
    """ Calculates the kspace trajectory from any gradient using Girf prediction and interpolates it on the adc raster
    """
    pass