import { useState } from "react";
import axios from "axios";

function RegistroVoluntario() {
  const [dados, setDados] = useState({
    nome: "",
    email: "",
    habilidades: "",
    disponibilidade: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://127.0.0.1:8000/api/voluntarios/", dados);
      alert("Perfil atualizado!");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="form-container">
      <h2>Completar Perfil Profissional</h2>
      <form onSubmit={handleSubmit} className="formulario-grid">
        <input
          type="text"
          placeholder="Nome Completo"
          required
          onChange={(e) => setDados({ ...dados, nome: e.target.value })}
        />
        <input
          type="email"
          placeholder="E-mail de Contato"
          required
          onChange={(e) => setDados({ ...dados, email: e.target.value })}
        />
        <textarea
          className="grid-span-2"
          placeholder="Descreva suas Habilidades (Tecnologia, Logística...)"
          required
          onChange={(e) => setDados({ ...dados, habilidades: e.target.value })}
        />
        <input
          className="grid-span-2"
          type="text"
          placeholder="Disponibilidade de Horário"
          required
          onChange={(e) =>
            setDados({ ...dados, disponibilidade: e.target.value })
          }
        />
        <button type="submit" className="btn-submit grid-span-2">
          Salvar Perfil
        </button>
      </form>
    </div>
  );
}
export default RegistroVoluntario;
