import crypto from 'crypto';
import 'dotenv/config';

const SERVER_PRIVATE_KEY = `-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQC38GGUc8TOS7FHUy98Rpm0jMLKrZoVrKH0q9kDMo2J/mPIdVmV
cTCT5NvKAebZdzv/Mq5DMcWr8xHij08uca4LyVDzijJXOQSxAV55TNXavEZhvFho
/lSt+nYOtO3xta3b9/8ruXKvqjZhESYR4dRn8Ilby+4OkA2N2iDCjyYIXwIDAQAB
AoGARikUr3FxMldA6bnbNQYg/vNqIbESQw40QIWEI2oW/vnfycipQQ2Jv//drjIH
gg+u/Oqx+cN0aOAwhECxrT+DaSk+X8DRBy9hghhuwemVttPDwPVj/Uvb+Mj2GCRN
5sMevRpeCQc2i6Wok3O6UzBi/LUZyG5yY95xmtc78l+C8pECQQDuRq4A5QXGA6mE
YdhgFKXaeWiwENwPYh8F4a+OvTUhZm7QZkT0xZ9YPijwXBdwG1JZm7brrtveLh+g
nY00jVEdAkEAxZ7/w4C6IG94u1g9THLhbLjAA+8K1efr/nFWNxEaIP4zxjdFi2Ss
PqxyQHnyeDa/m1Oq+iXRa0Hp4lrnkfciqwJBALyOpigDFLyMLVubanUuIclwBk4+
KUbrKQ2oeRsF08Ooocy9AZiJwv07w33iApIurM5IkUqUx11dNp4Nz65knmkCQH/X
Z+V1NPMeqZ+oaZ83AhVvPuhMj1npeoVTlE5zRc/qIlwsDVUrfzHcJN0JBo41/KXi
7kx8gok8Tq0b2YpXsZkCQCjDYlOuXUOdsMEGjZJvyzL60jBZ0acpYTfQ3yDEqu33
pH7DdYHF5fWP0udUbK1pUuQ+DgSchcg65hDGUm8rjHQ=
-----END RSA PRIVATE KEY-----`;

const SERVER_PUBLIC_KEY = `-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC38GGUc8TOS7FHUy98Rpm0jMLK
rZoVrKH0q9kDMo2J/mPIdVmVcTCT5NvKAebZdzv/Mq5DMcWr8xHij08uca4LyVDz
ijJXOQSxAV55TNXavEZhvFho/lSt+nYOtO3xta3b9/8ruXKvqjZhESYR4dRn8Ilb
y+4OkA2N2iDCjyYIXwIDAQAB
-----END PUBLIC KEY-----`;

export const decrypt = (data: string) => {
  const decrypted = crypto.privateDecrypt(
    {
      key: SERVER_PRIVATE_KEY,
      passphrase: '',
    },
    Buffer.from(data, 'base64')
  );
  return decrypted.toString('utf8');
};

export const encrypt = (data: string) => {
  const encrypted = crypto.publicEncrypt(
    {
      key: SERVER_PUBLIC_KEY,
      padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
      oaepHash: 'sha256',
    },
    Buffer.from(data)
  );
  return encrypted.toString('base64');
};
