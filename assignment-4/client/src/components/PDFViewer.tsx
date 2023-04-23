import React from 'react';
import { Viewer, Worker } from '@react-pdf-viewer/core';
import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout';

import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';

type Props = {
  buffer: Uint8Array;
};

export const PDFViewer = ({ buffer }: Props) => {
  const defaultLayoutPluginInstance = defaultLayoutPlugin();

  return (
    <div>
      <Worker workerUrl='https://unpkg.com/pdfjs-dist@2.15.349/build/pdf.worker.js'>
        <div style={{ height: '1000px', width: '750px' }}>
          <Viewer fileUrl={buffer} plugins={[defaultLayoutPluginInstance]} />
        </div>
      </Worker>
    </div>
  );
};
