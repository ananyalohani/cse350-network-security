import { format } from 'date-fns';
import { User } from '../types/auth';

export const generateCertificateTemplate = (user: User, timestamp: Date) => {
  const datetime = format(timestamp, 'dd/MM/yyyy HH:mm:ss');
  return `<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Hello world!</title>
  </head>
  <body>
    <style>
      body {
        font-size: 12px;
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
      div.sign {
        margin-top: 100px;
        color: rgb(204, 0, 0);
        width: 100%;
      }
      p.sign1 {
        font-weight: normal;
      }
      p.sign2 {
        margin-top: 100px;
        font-weight: normal;
      }
      div.details {
        margin-top: 20px;
        margin-bottom: 30px;
      }
    </style>
    <h1>Degree Certificate</h1>
    <h2>2019-2023 Session</h2>
    <div class="details">
      <p><span>Name: </span>${user.name}</p>
      <p><span>Roll Number: </span>${user.username}</p>
    </div>
    <p>To whoever this may concern,</p>
    <p>
      This is to certify that ${user.name} has successfully graduated from
      Indraprastha Institute of Information Technology, Delhi with a Bachelor of
      Technology degree in the field of Computer Science and Engineering.
    </p>
    <div class="sign">
      <p class="sign1">Signed by Director IIITD on ${datetime}</p>
      <p class="sign2">Signed by Registrar IIITD on ${datetime}</p>
    </div>
  </body>
</html>
`;
};

export const generateTranscriptTemplate = (user: User, timestamp: Date) => {
  const datetime = format(timestamp, 'dd/MM/yyyy HH:mm:ss');
  return `<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Hello world!</title>
  </head>
  <body>
    <style>
      body {
        font-size: 12px;
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
      div.sign {
        margin-top: 100px;
        color: rgb(204, 0, 0);
        width: 100%;
      }
      p.sign1 {
        font-weight: normal;
      }
      p.sign2 {
        margin-top: 100px;
        font-weight: normal;
      }
      div.details {
        margin-top: 20px;
        margin-bottom: 30px;
      }
    </style>
    <h1>Transcript</h1>
    <h2>Semester 8: Jan-May 2023</h2>
    <div class="details">
      <p><span>Name: </span>${user.name}</p>
      <p><span>Roll Number: </span>${user.username}</p>
    </div>
    <table>
      <thead>
        <tr>
          <th>Semester</th>
          <th>Grade</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Monsoon 2019 (Semester 1)</td>
          <td>A</td>
        </tr>
        <tr>
          <td>Winter 2020 (Semester 2)</td>
          <td>A</td>
        </tr>
        <tr>
          <td>Monsoon 2020 (Semester 3)</td>
          <td>A</td>
        </tr>
        <tr>
          <td>Winter 2021 (Semester 4)</td>
          <td>A</td>
        </tr>
        <tr>
          <td>Monsoon 2021 (Semester 5)</td>
          <td>A</td>
        </tr>
        <tr>
          <td>Winter 2022 (Semester 6)</td>
          <td>A</td>
        </tr>
        <tr>
          <td>Monsoon 2022 (Semester 7)</td>
          <td>A</td>
        </tr>
        <tr>
          <td>Winter 2023 (Semester 8)</td>
          <td>A</td>
        </tr>
        <tr>
          <td><b>Final Grade</b></td>
          <td><b>A</b></td>
        </tr>
      </tbody>
    </table>
    <div class="sign">
      <p class="sign1">Signed by Director IIITD on ${datetime}</p>
      <p class="sign2">Signed by Registrar IIITD on ${datetime}</p>
    </div>
  </body>
</html>
`;
};
