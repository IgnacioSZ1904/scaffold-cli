import { app } from './app.js';

const port = process.env.PORT || 3000;

app.listen(port, () => {
  console.log('$project_name escuchando en http://localhost:' + port);
});
