import {
  generateCertificateTemplate,
  generateTranscriptTemplate,
} from './templates';
import { Role, User } from '../types/auth';
import { users } from '../data/users';

declare var require: any;

export const generatePdfForStudents = async () => {
  const students = users.filter((user) => user.role === Role.STUDENT);
  const transcriptPromises = students.map((student) =>
    generateTranscript(student)
  );
  const certificatePromises = students.map((student) =>
    generateCertificate(student)
  );
  await Promise.all([...transcriptPromises, ...certificatePromises]);
};

const generateTranscript = async (user: User) => {
  const pdf = require('pdf-creator-node');
  const html = generateTranscriptTemplate(user);
  const options = {
    format: 'A4',
    orientation: 'portrait',
    border: '10mm',
  };
  const document = {
    html: html,
    data: {},
    path: `files/transcripts/${user.username}.pdf`,
    type: '',
  };
  const res = await pdf.create(document, options);
  return res;
};

const generateCertificate = async (user: User) => {
  const pdf = require('pdf-creator-node');
  const html = generateCertificateTemplate(user);
  const options = {
    format: 'A4',
    orientation: 'portrait',
    border: '10mm',
  };
  const document = {
    html: html,
    data: {},
    path: `files/certificates/${user.username}.pdf`,
    type: '',
  };
  const res = await pdf.create(document, options);
  return res;
};
