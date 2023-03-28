import pydicom
import numpy as np
from PIL import Image
from datetime import date


class Dicom:
    def load_image(dicom_file):
        img = dicom_file.pixel_array.astype(float)
        rescaled_img = (np.maximum(img, 0) / img.max()) * 255
        final_img = np.uint8(rescaled_img)
        final_img = Image.fromarray(final_img)
        return final_img

    def load_file(path):
        Dicom = pydicom.dcmread(path)
        patientData = {}
        patientData['PatientName'] = Dicom['PatientName'].value
        patientData['StudyDate'] = Dicom['StudyDate'].value
        patientData['StudyDescription'] = Dicom['StudyDescription'].value
        patientData['Image'] = Dicom.load_image(Dicom)
        return patientData

    def save_file(patientData, path):
        img = np.asarray(patientData['Image'])
        Dicom = pydicom.dcmread('Input/Dicom/dicom.dcm')

        Dicom.PatientName = patientData['PatientName']
        Dicom.StudyDate = Dicom.convert_date(patientData['StudyDate'])
        Dicom.StudyDescription = patientData['StudyDescription']
        Dicom.PixelData = patientData['Image'].tobytes()

        Dicom.Rows = img.shape[0]
        Dicom.Columns = img.shape[1]
        Dicom.SamplesPerPixel = 1
        Dicom.BitsStored = 8
        Dicom.BitsAllocated = 8
        Dicom.HighBit = 7
        Dicom.PixelRepresentation = 0

        Dicom.save_as(path)

    def convert_date(date):
        return date.strftime('%Y%m%d')


if __name__ == '__main__':
    # Loading from dicom file example
    path = 'Input/Dicom/dicom.dcm'
    patientData = Dicom.load_file(path)
    img = patientData['Image']
    #img.save('original_img.jpg')

    # Saving as dicom file example
    studyDate = date(year=2022, month=5, day=10)
    img = Image.open('Input/Img/Kwadraty2.jpg').convert('L')
    patientData = {'PatientName': 'Jakub Czarnecki', 'StudyDescription': 'TK Glowy', 'Image': img,
                   'StudyDate': studyDate}
    Dicom.save_file(patientData, 'Output/Dicom/new_dicom.dcm')
