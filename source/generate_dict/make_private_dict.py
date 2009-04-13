# make_private_dict.py
"""Take private.dic file from mdcm project and convert 
to python dict, write that to a file as python code.
This is a one-time operation unless updates to the input file happen.
The generated .py file becomes part of the pydicom distribution.
"""
# Copyright 2008, Darcy Mason
# This file is part of pydicom.
# Generates output from a file from the MDCM project (http://code.google.com/p/mdcm),
# which in turn is based on dcmtk and gdcm.
# See the license.txt file for license information.

from csv2dict import write_dict
import pprint

in_filename = "mdcm-r52-private.dic"
pydict_filename = "../dicom/_private_dict.py"
dict_name = "private_dictionaries"

if __name__ == "__main__":
    # Read the MDCM formatted file, with the following tab-separated format:
    #    group el VR name   creator
    #  (there are two tabs before creator)
    # and compose a dictionary of dictionaries in memory
    #   (dict of each creator name mapped to dict of dicom attributes
    #                                                        for that creator)

    in_file = open(in_filename, 'rb')

    creator_dicts = {}
    for line in in_file:
        # Ignore comments
        if line.startswith("#"):
            continue
        # Parse a single attribute line
        group, element, VR, VM, name, skip, creator = line.strip().split("\t")
        # Compose group-element tag into one long integer
        tag = group.strip() + element.strip()
        # If don't have creator yet, initialize it's DICOM dict
        if creator not in creator_dicts:
            creator_dicts[creator] = {}
        # Add current DICOM attribute to the creator's dict
        # Make as similar as possible to the non-private DICOM dictionaries
        #    that pydicom uses (VR, VM, name, isRetired); no VM or retired so blank
        creator_dicts[creator][tag] = (VR, '', name, '')

    # Send the dictionary of dictionaries to a python file (after header comments)
    out_doc = """# %(filename)s
# Copyright 2009, Darcy Mason
# This file is part of pydicom.
# Autogenerated by make_private_dict.py,
# from private.dic file of mdcm library (http://code.google.com/p/mdcm),
# which in turn is based on dcmtk and gdcm.
# See the license.txt file for license information on pydicom, mdcm, and dcmtk
 
# This is a dictionary of DICOM dictionaries. 
# The outer dictionary key is the Private Creator name,
#   the inner dictionary is a map of DICOM tag to (VR, type, name, isRetired)
"""
    py_file = open(pydict_filename, "wb")
    py_file.write(out_doc % {'filename': pydict_filename})
    py_file.write("%s = \\\n" % dict_name)
    pprint.pprint(creator_dicts, py_file)
    py_file.close()

    print "Finished creating python file %s containing the private dictionaries" % pydict_filename