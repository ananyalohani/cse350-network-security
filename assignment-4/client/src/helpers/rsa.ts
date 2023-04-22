import crypto from 'crypto';

const SERVER_PUBLIC_KEY = `-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC38GGUc8TOS7FHUy98Rpm0jMLK
rZoVrKH0q9kDMo2J/mPIdVmVcTCT5NvKAebZdzv/Mq5DMcWr8xHij08uca4LyVDz
ijJXOQSxAV55TNXavEZhvFho/lSt+nYOtO3xta3b9/8ruXKvqjZhESYR4dRn8Ilb
y+4OkA2N2iDCjyYIXwIDAQAB
-----END PUBLIC KEY-----`;

export const encrypt = (data: string) => {
  const encrypted = crypto.publicEncrypt(
    {
      key: SERVER_PUBLIC_KEY,
      passphrase: '',
      padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
      oaepHash: 'sha256',
    },
    Buffer.from(data)
  );
  return encrypted.toString('base64');
};
