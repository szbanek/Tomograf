import pydicom
import numpy as np
from PIL import Image
from datetime import date


class Dicom:
    def load_image(self, dicom_file):
        img = dicom_file.pixel_array.astype(float)
        rescaled_img = (np.maximum(img, 0) / img.max()) * 255
        final_img = np.uint8(rescaled_img)
        final_img = Image.fromarray(final_img)
        return final_img

    def load_file(self, path):
        ds = pydicom.dcmread(path)
        patientData = {}
        patientData['PatientName'] = ds['PatientName'].value
        patientData['StudyDate'] = ds['StudyDate'].value
        patientData['StudyDescription'] = ds['StudyDescription'].value
        patientData['Image'] = self.load_image(ds)
        return patientData

    def save_file(self, patientData, path):
        img = np.asarray(patientData['Image'])
        ds = pydicom.dcmread('Input/Dicom/dicom.dcm')

        ds.PatientName = patientData['PatientName']
        ds.StudyDate = self.convert_date(patientData['StudyDate'])
        ds.StudyDescription = patientData['StudyDescription']
        ds.PixelData = patientData['Image'].tobytes()

        ds.Rows = img.shape[0]
        ds.Columns = img.shape[1]
        ds.SamplesPerPixel = 1
        ds.BitsStored = 8
        ds.BitsAllocated = 8
        ds.HighBit = 7
        ds.PixelRepresentation = 0

        ds.save_as(path)

    def convert_date(self, date):
        return date.strftime('%Y%m%d')


if __name__ == '__main__':
    ds = Dicom()
    # Loading from dicom file example
    path = 'Input/Dicom/dicom.dcm'
    patientData = ds.load_file(path)
    img = patientData['Image']
    #img.save('original_img.jpg')

    # Saving as dicom file example
    studyDate = date(year=2022, month=5, day=10)
    img = Image.open('Input/Img/Kwadraty2.jpg').convert('L')
    patientData = {'PatientName': 'Jakub Czarnecki', 'StudyDescription': 'TK Glowy', 'Image': img,
                   'StudyDate': studyDate}
    ds.save_file(patientData, 'Output/Dicom/new_dicom.dcm')
