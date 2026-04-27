import { useState } from "react";
import axios from "axios";

function RegistroCrise() {
  const [crise, setCrise] = useState({ titulo: "", descricao_bruta: "" });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post("http://127.0.0.1:8000/api/crises/", crise);
      alert("Crise registrada! A IA está processando as necessidades.");
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2>Registrar Emergência</h2>
      <form onSubmit={handleSubmit} className="formulario-grid">
        <input
          className="grid-span-2"
          type="text"
          placeholder="Título Breve"
          required
          onChange={(e) => setCrise({ ...crise, titulo: e.target.value })}
        />
        <textarea
          className="grid-span-2"
          rows="5"
          placeholder="Descreva a situação em texto livre. A IA organizará os dados."
          required
          onChange={(e) =>
            setCrise({ ...crise, descricao_bruta: e.target.value })
          }
        />
        <button
          type="submit"
          className="btn-submit btn-alerta grid-span-2"
          disabled={loading}
        >
          {loading ? "Processando no watsonx..." : "Enviar Alerta de Crise"}
        </button>
      </form>
    </div>
  );
}
export default RegistroCrise;
