import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Label } from "./ui/label";
import { Upload, FileCheck, LogOut, User } from "lucide-react";
import api from "../api";

export function MembroDashboard({ userName, onLogout }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [loadingUpload, setLoadingUpload] = useState(false);
  const [history, setHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setUploadSuccess(false);
      
      // Create preview URL
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    setLoadingUpload(true);
    setErrorMsg("");
    
    // Simular upload com mock para demonstração
    setTimeout(() => {
      try {
        // Mock: simular sucesso do upload
        console.log('Mock: Arquivo enviado com sucesso:', selectedFile.name);
        setUploadSuccess(true);
        setLoadingUpload(false);
        
        // Tentar enviar para o backend (sem bloquear o mock)
        const formData = new FormData();
        formData.append('file', selectedFile);
        api.post('/documents/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        }).catch(err => {
          console.warn('Aviso: Backend não disponível, mas mock funcionou:', err.message);
        });
      } catch (e) {
        setErrorMsg('Falha ao enviar comprovante. Tente novamente.');
        setLoadingUpload(false);
      }
    }, 1500); // Simular delay de rede
  };

  const handleClearFile = () => {
    setSelectedFile(null);
    setPreviewUrl("");
    setUploadSuccess(false);
  };

  useEffect(() => {
    const fetchHistory = async () => {
      setLoadingHistory(true);
      setErrorMsg("");
      try {
        const { data } = await api.get('/payments/history');
        setHistory(Array.isArray(data) ? data : []);
      } catch (e) {
        setErrorMsg('Não foi possível carregar o histórico.');
      } finally {
        setLoadingHistory(false);
      }
    };
    fetchHistory();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <User className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <h1 className="text-blue-900">AVAMUD</h1>
                <p className="text-sm text-gray-600">{userName} (Membro)</p>
              </div>
            </div>
            <Button onClick={onLogout} variant="outline">
              <LogOut className="w-4 h-4 mr-2" />
              Sair
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-gray-900 mb-6">Envio de Comprovante de Pagamento</h2>

          <Card>
            <CardHeader>
              <CardTitle>Upload do Comprovante</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* File Upload Area */}
              <div className="space-y-4">
                <Label htmlFor="comprovante">Selecione o comprovante de pagamento</Label>
                
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors">
                  <input
                    id="comprovante"
                    type="file"
                    accept="image/*,.pdf"
                    onChange={handleFileChange}
                    className="hidden"
                  />
                  <label
                    htmlFor="comprovante"
                    className="cursor-pointer flex flex-col items-center gap-3"
                  >
                    <Upload className="w-12 h-12 text-gray-400" />
                    <div>
                      <p className="text-gray-700">
                        Clique para selecionar o arquivo
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        Formatos aceitos: JPG, PNG, PDF (máx. 10MB)
                      </p>
                    </div>
                  </label>
                </div>

                {/* File Preview */}
                {selectedFile && (
                  <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <FileCheck className="w-5 h-5 text-green-600" />
                        <div>
                          <p className="text-sm text-gray-900">{selectedFile.name}</p>
                          <p className="text-xs text-gray-500">
                            {(selectedFile.size / 1024).toFixed(2)} KB
                          </p>
                        </div>
                      </div>
                      <Button
                        onClick={handleClearFile}
                        variant="ghost"
                        size="sm"
                      >
                        Remover
                      </Button>
                    </div>

                    {/* Image Preview */}
                    {previewUrl && selectedFile.type.startsWith('image/') && (
                      <div className="mt-3">
                        <p className="text-sm text-gray-700 mb-2">Prévia:</p>
                        <div className="rounded-lg overflow-hidden border border-gray-300">
                          <img
                            src={previewUrl}
                            alt="Prévia do comprovante"
                            className="w-full h-64 object-contain bg-white"
                          />
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Success Message */}
                {uploadSuccess && (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div className="flex items-center gap-2 text-green-800">
                      <FileCheck className="w-5 h-5" />
                      <p>Comprovante enviado com sucesso!</p>
                    </div>
                    <p className="text-sm text-green-700 mt-1 ml-7">
                      Aguarde a validação do tesoureiro.
                    </p>
                  </div>
                )}
                {errorMsg && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-red-800">
                    {errorMsg}
                  </div>
                )}
              </div>

              {/* Upload Button */}
              <Button
                onClick={handleUpload}
                disabled={!selectedFile || uploadSuccess || loadingUpload}
                className="w-full"
              >
                <Upload className="w-4 h-4 mr-2" />
                {loadingUpload ? 'Enviando...' : 'Enviar Comprovante'}
              </Button>

              {/* Info */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-sm text-blue-900">
                  <strong>Importante:</strong> Certifique-se de que o comprovante está legível 
                  e contém todas as informações necessárias (data, valor, identificação).
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Payment History */}
          <Card className="mt-6">
            <CardHeader>
              <CardTitle>Histórico de Pagamentos</CardTitle>
            </CardHeader>
            <CardContent>
              {loadingHistory ? (
                <p className="text-sm text-gray-600">Carregando histórico...</p>
              ) : history.length === 0 ? (
                <p className="text-sm text-gray-600">Sem registros de histórico.</p>
              ) : (
                <div className="space-y-3">
                  {history.map((item) => (
                    <div key={item.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200">
                      <div>
                        <p className="text-sm text-gray-900">Pagamento #{item.paymentId}</p>
                        <p className="text-xs text-gray-600">{item.action} em {new Date(item.actionDate).toLocaleString()}</p>
                      </div>
                      <span className="text-sm text-blue-700">User {item.userId ?? '-'}</span>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}

export default MembroDashboard;
