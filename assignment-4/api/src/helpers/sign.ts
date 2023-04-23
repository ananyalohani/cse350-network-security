import path from 'path';
import fs from 'fs';
import {
  plainAddPlaceholder,
  extractSignature,
  // @ts-ignore
} from 'node-signpdf/dist/helpers';
// @ts-ignore
import signer from 'node-signpdf/dist/signpdf';

export const directorSign = (filepath: string) => {
  const p12Buffer = fs.readFileSync(
    path.resolve(__dirname, '../../keys/director.p12')
  );
  let pdfBuffer = fs.readFileSync(
    path.resolve(__dirname, '../../files/transcripts/' + filepath)
  );
  pdfBuffer = plainAddPlaceholder({
    pdfBuffer,
    reason: 'I am the director',
    location: 'IIIT Delhi',
    name: 'Director',
    contactInfo: 'director@iiitd.ac.in',
    signatureLength: 4096,
  });
  pdfBuffer = signer.sign(pdfBuffer, p12Buffer);
  const { signature, signedData } = extractSignature(pdfBuffer);
  fs.writeFileSync(
    path.resolve(__dirname, '../../files/transcripts/' + filepath),
    pdfBuffer
  );
  return { signature, signedData, pdfBuffer };
};

export const registrarSign = (filepath: string) => {
  const p12Buffer = fs.readFileSync(
    path.resolve(__dirname, '../../keys/registrar.p12')
  );
  let pdfBuffer = fs.readFileSync(
    path.resolve(__dirname, '../../files/transcripts/' + filepath)
  );
  pdfBuffer = plainAddPlaceholder({
    pdfBuffer,
    reason: 'I am the registrar',
    location: 'IIIT Delhi',
    name: 'Registrar',
    contactInfo: 'registrar@iiitd.ac.in',
    signatureLength: 4096,
  });
  pdfBuffer = signer.sign(pdfBuffer, p12Buffer);
  const { signature, signedData } = extractSignature(pdfBuffer);
  fs.writeFileSync(
    path.resolve(__dirname, '../../files/transcripts/' + filepath),
    pdfBuffer
  );
  return { signature, signedData, pdfBuffer };
};
