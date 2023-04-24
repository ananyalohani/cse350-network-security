import fs from 'fs';
import {
  extractSignature,
  plainAddPlaceholder,
  // @ts-ignore
} from 'node-signpdf/dist/helpers';
import path from 'path';
// @ts-ignore
import signer from 'node-signpdf/dist/signpdf';
import { PDFDocument, StandardFonts } from 'pdf-lib';

export const directorSign = async (filepath: string) => {
  const p12Buffer = fs.readFileSync(
    path.resolve(__dirname, '../../keys/director.p12')
  );
  let pdfBuffer = fs.readFileSync(
    path.resolve(__dirname, '../../files/transcripts/' + filepath)
  );
  pdfBuffer = plainAddPlaceholder({
    pdfBuffer,
    reason: 'Verified by the director',
    location: 'IIIT Delhi',
    name: 'Director',
    contactInfo: 'director@iiitd.ac.in',
    signatureLength: 4096,
  });
  pdfBuffer = signer.sign(pdfBuffer, p12Buffer);
  const timestamp = new Date();
  const { signature, signedData } = extractSignature(pdfBuffer);
  fs.writeFileSync(
    path.resolve(__dirname, '../../files/transcripts/' + filepath),
    pdfBuffer
  );
  return { timestamp, signature, signedData };
};

export const registrarSign = async (filepath: string) => {
  const p12Buffer = fs.readFileSync(
    path.resolve(__dirname, '../../keys/registrar.p12')
  );
  let pdfBuffer = fs.readFileSync(
    path.resolve(__dirname, '../../files/transcripts/' + filepath)
  );
  pdfBuffer = plainAddPlaceholder({
    pdfBuffer,
    reason: 'Verified by the registrar',
    location: 'IIIT Delhi',
    name: 'Registrar',
    contactInfo: 'registrar@iiitd.ac.in',
    signatureLength: 4096,
  });
  pdfBuffer = signer.sign(pdfBuffer, p12Buffer);
  const timestamp = new Date();
  const { signature, signedData } = extractSignature(pdfBuffer);
  fs.writeFileSync(
    path.resolve(__dirname, '../../files/transcripts/' + filepath),
    pdfBuffer
  );
  return { timestamp, signature, signedData };
};

export const addWatermark = async (
  filepath: string,
  watermark: string,
  position: 'bottom-left' | 'bottom-right'
) => {
  const pdfBuffer = fs.readFileSync(
    path.resolve(__dirname, '../../files/transcripts/' + filepath)
  );
  const pdfDoc = await PDFDocument.load(pdfBuffer);
  const pages = pdfDoc.getPages();
  const firstPage = pages[0];
  const helveticaFont = await pdfDoc.embedFont(StandardFonts.Helvetica);
  const x = position === 'bottom-right' ? 320 : 20;
  const y = 20;
  firstPage.drawText(watermark, {
    x,
    y,
    size: 12,
    font: helveticaFont,
  });
  const pdfBytes = await pdfDoc.save();
  fs.writeFileSync(
    path.resolve(__dirname, '../../files/transcripts/' + filepath),
    pdfBytes
  );
  return pdfBytes;
};
