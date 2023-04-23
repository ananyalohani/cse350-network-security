import { Role, User } from '../../types/auth';
import { users } from '../../data/users';

declare var require: any;

export const generatePdfForStudents = async () => {
  const students = users.filter((user) => user.role === Role.STUDENT);
  const promises = students.map((student) => generatePdf(student));
  await Promise.all(promises);
};

const generatePdf = async (user: User) => {
  const pdf = require('pdf-creator-node');
  const html = generateTemplate(user);
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

const generateTemplate = (user: User) => {
  return `<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Hello world!</title>
  </head>
  <body>
    <style>
      body {
        font-family: sans-serif;
        padding: 80px 60px;
      }
      h1 {
        text-align: center;
        font-weight: bold;
        margin: 0;
        margin-bottom: 3px;
        padding: 0;
      }
      h2 {
        text-align: center;
        font-weight: normal;
        margin: 0;
        margin-bottom: 10px;
        padding: 0;
        color: darkslategray;
      }
      p {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
      }
      table {
        margin-top: 20px;
        width: 100%;
        border: solid 1px #dfdfdf;
        border-collapse: collapse;
      }
      thead {
        background: #cfcfcf;
      }
      th {
        padding: 5px 3px;
        border: solid 1px #dfdfdf;
        text-align: left;
      }
      p > span {
        font-weight: bold;
      }
      td {
        padding: 5px 3px;
        border: solid 1px #dfdfdf;
      }
      input {
        opacity: 0;
      }
    </style>
    <h1>Transcript</h1>
    <h2>Semester 8: Jan-May 2023</h2>
    <div>
      <p><span>Name: </span>${user.name}</p>
      <p><span>Roll Number: </span>${user.username}</p>
    </div>
    <table>
      <thead>
        <tr>
          <th>Course Name</th>
          <th>Grade</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Network Security</td>
          <td>A</td>
        </tr>
        <tr>
          <td>Distributed Systems</td>
          <td>A</td>
        </tr>
        <tr>
          <td>Fundamentals of Audio</td>
          <td>A</td>
        </tr>
        <tr>
          <td>Attention and Perception</td>
          <td>A</td>
        </tr>
        <tr>
          <td><b>Final Grade</b></td>
          <td><b>A</b></td>
        </tr>
      </tbody>
    </table>
    <form>
      <input type="text" name="signature" />
      <input type="text" name="signature" />
    </form>
  </body>
</html>
`;
};
