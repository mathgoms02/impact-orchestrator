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
      alert("Perfil profissional atualizado!");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2>Seu Perfil de Voluntariado</h2>
        <p>
          Mantenha suas habilidades atualizadas para precisão na orquestração.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="form-grid">
        <div className="input-group">
          <label>Nome Completo</label>
          <input
            type="text"
            placeholder="Como deseja ser chamado"
            required
            onChange={(e) => setDados({ ...dados, nome: e.target.value })}
          />
        </div>

        <div className="input-group">
          <label>E-mail de Contato</label>
          <input
            type="email"
            placeholder="seu@email.com"
            required
            onChange={(e) => setDados({ ...dados, email: e.target.value })}
          />
        </div>

        <div className="input-group span-2">
          <label>Habilidades Técnicas e Práticas</label>
          <textarea
            rows="3"
            placeholder="Ex: Programação, Logística, Enfermagem, Motorista..."
            required
            onChange={(e) =>
              setDados({ ...dados, habilidades: e.target.value })
            }
          />
        </div>

        <div className="input-group span-2">
          <label>Disponibilidade de Tempo</label>
          <input
            type="text"
            placeholder="Ex: Finais de semana, Horário comercial..."
            required
            onChange={(e) =>
              setDados({ ...dados, disponibilidade: e.target.value })
            }
          />
        </div>

        <button type="submit" className="btn btn-primary span-2">
          Salvar Informações
        </button>
      </form>
    </div>
  );
}
export default RegistroVoluntario;
