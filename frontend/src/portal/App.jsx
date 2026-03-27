import React, { useMemo, useState } from 'react'
import './style.css'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const I18N = {
  en: {
    // nav/cta
    nav_cta: 'Get Started',
    home: 'Home',
    purpose_options: [
      'Earth Observation',
      'Technology Development',
      'Communications',
      'Earth Science',
      'Space Science',
      'Space Science/Technology Demonstration',
      'Communications/Technology Development',
      'Communications/Maritime Tracking',
      'Technology Demonstration',
      'Navigation/Global Positioning',
      'Earth Observation/Technology Development',
      'Earth Observation/Communications',
      'Earth/Space Observation',
      'Educational',
      'Earth Observation/Earth Science',
      'Platform',
      'Earth Observation/Space Science',
      'Earth Observation/Navigation',
      'Communications/Navigation',
      'Space Observation',
      'Surveillance',
      'Navigation/Regional Positioning',
      'Space Science/Technology Development',
      'Mission Extension Technology',
      'Earth Science/Earth Observation',
      'Earth Observation/Communications/Space Science',
      'Meteorological',
      'Technology Development/Educational',
      'Satellite Positioning',
      'Other'
    ],
    // hero
    badge: '⚡ Open Beta • APIs & Samples',
    hero_title: '<span class="neon">Satellite Data Request Portal</span><br/>for a smarter, more sustainable planet.',
    hero_sub: 'Submit your request and instantly browse satellites ranked by sustainability.',
    chip_carbon: '🌿 Carbon‑aware', chip_sats: '🛰️ 1200+ satellites', chip_samples: '📦 Samples included',
    // request section
    portal_kicker: 'Client request', portal_title: 'Submit your data request',
    portal_instructions: 'To make your request: Fill in the data below. Select an Ecological Classification. Define a Delivery method. Filter the Satellites.',
    client_title: 'Client Information', name: 'Name', cnpj: 'Company ID', address: 'Address',
    email: 'Email', email_hint: 'Primary contact email for this request.',
    sector: 'Business sector', sector_hint: 'Requester industry or activity.',
    sector_options: ['Academic','Agribusiness','Climate','Industrial','Military','Scientific','Other'],
    name_hint: 'Requester full name or organization contact.',
    cnpj_hint: 'Company identification number (CNPJ or equivalent).',
    address_hint: 'Billing or correspondence address.',
    request_title: 'Request', purpose: 'Purpose', purpose_hint: 'High-level intended use of the requested satellite data.', classification: 'Ecological classification', classification_hint: 'Select the sustainability rank (GOLD, SILVER, BRONZE) derived from environmental criteria.', delivery: 'Delivery', delivery_hint: 'Choose how the data will be delivered (API or batch files).', description: 'Description', description_hint: 'Add details to scope the request (AOI, cadence, formats, constraints).',
    country: 'Country', country_hint: 'Select the requester country.',
    other_label: 'Other', other_placeholder: 'Describe the purpose', other_hint: 'Provide the purpose if it is not listed.', specify_other: 'Specify purpose',
    filter_btn: 'Filter Satellites', submit_btn: 'Submit Request', satellites: 'Satellites (sample)',
    no_results: 'No results',
    loading: 'Loading...',
    // toasts
    toast_ok: 'Request saved'
  },
  pt: {
    nav_cta: 'Começar',
    home: 'Início',
    purpose_options: [
      'Observação da Terra',
      'Desenvolvimento de Tecnologia',
      'Comunicações',
      'Ciências da Terra',
      'Ciências Espaciais',
      'Ciências Espaciais/Demonstração Tecnológica',
      'Comunicações/Desenvolvimento de Tecnologia',
      'Comunicações/Rastreamento Marítimo',
      'Demonstração Tecnológica',
      'Navegação/Posicionamento Global',
      'Observação da Terra/Desenvolvimento de Tecnologia',
      'Observação da Terra/Comunicações',
      'Observação da Terra/Espaço',
      'Educacional',
      'Observação da Terra/Ciências da Terra',
      'Plataforma',
      'Observação da Terra/Ciências Espaciais',
      'Observação da Terra/Navegação',
      'Comunicações/Navegação',
      'Observação Espacial',
      'Vigilância',
      'Navegação/Posicionamento Regional',
      'Ciências Espaciais/Desenvolvimento de Tecnologia',
      'Tecnologia de Extensão de Missão',
      'Ciências da Terra/Observação da Terra',
      'Observação da Terra/Comunicações/Ciências Espaciais',
      'Meteorológico',
      'Desenvolvimento de Tecnologia/Educacional',
      'Posicionamento por Satélite',
      'Outro'
    ],
    badge: '⚡ Beta Aberto • APIs e Amostras',
    hero_title: '<span class="neon">Portal de Solicitação de Dados</span><br/>para um planeta mais inteligente e sustentável.',
    hero_sub: 'Envie sua solicitação e navegue por satélites ranqueados por sustentabilidade.',
    chip_carbon: '🌿 Carbon‑aware', chip_sats: '🛰️ 1200+ satélites', chip_samples: '📦 Amostras incluídas',
    portal_kicker: 'Solicitação do cliente', portal_title: 'Envie sua solicitação de dados',
    portal_instructions: 'Para fazer a sua Requisição: Preencha os dados abaixo. Selecione uma Classificação Ecológica. Defina uma forma de Entrega. Filtre os Satélites.',
    client_title: 'Dados do Cliente', name: 'Nome', cnpj: 'CNPJ', address: 'Endereço',
    email: 'Email', email_hint: 'Email de contato principal desta solicitação.',
    sector: 'Ramo de atividade', sector_hint: 'Setor/atividade do solicitante.',
    sector_options: ['Acadêmico','Agronegócio','Climático','Industrial','Militar','Científico','Outro'],
    name_hint: 'Nome completo do solicitante ou contato da organização.',
    cnpj_hint: 'Identificação da empresa (CNPJ ou equivalente).',
    address_hint: 'Endereço para cobrança ou correspondência.',
    request_title: 'Solicitação', purpose: 'Finalidade', purpose_hint: 'Uso pretendido dos dados de satélite em alto nível.', classification: 'Classificação ecológica', classification_hint: 'Escolha o nível de sustentabilidade (OURO, PRATA, BRONZE) calculado por critérios ambientais.', delivery: 'Entrega', delivery_hint: 'Como os dados serão entregues (API ou arquivos em lote).', description: 'Descrição', description_hint: 'Inclua detalhes para escopo (AOI, periodicidade, formatos, restrições).',
    country: 'País', country_hint: 'Selecione o país do solicitante.',
    other_label: 'Outro', other_placeholder: 'Descreva a finalidade', other_hint: 'Informe a finalidade caso não esteja listada.', specify_other: 'Especificar finalidade',
    filter_btn: 'Filtrar Satélites', submit_btn: 'Enviar Solicitação', satellites: 'Satélites (amostra)',
    no_results: 'Sem resultados',
    loading: 'Carregando...',
    toast_ok: 'Solicitação registrada'
  }
}

function classBadge(label, lang='en'){
  const L = (label||'').toUpperCase()
  const isPending = (L==='PENDENTE DE CLASSIFICAÇÃO' || L==='PENDING' || L==='PENDING CLASSIFICATION')
  const cls = isPending
    ? 'silver'
    : (L==='OURO' || L==='GOLD' ? 'gold' : (L==='PRATA' || L==='SILVER' ? 'silver' : 'bronze'))
  
  // Translate the label based on the selected language
  let displayLabel = L
  if (lang === 'pt') {
    if (L === 'GOLD') displayLabel = 'OURO'
    else if (L === 'SILVER') displayLabel = 'PRATA'
    else if (L === 'BRONZE') displayLabel = 'BRONZE'
    else if (L === 'PENDING' || L === 'PENDING CLASSIFICATION') displayLabel = 'PENDENTE DE CLASSIFICAÇÃO'
  } else {
    if (L === 'OURO') displayLabel = 'GOLD'
    else if (L === 'PRATA') displayLabel = 'SILVER'
    else if (L === 'BRONZE') displayLabel = 'BRONZE'
    else if (L === 'PENDENTE DE CLASSIFICAÇÃO') displayLabel = 'PENDING CLASSIFICATION'
  }
  
  return <span className={`badge-class ${cls}`}>{displayLabel}</span>
}

const CLASS_VALUES = ['OURO','PRATA','BRONZE','PENDENTE DE CLASSIFICAÇÃO']
const CLASS_LABELS_PT = ['OURO','PRATA','BRONZE','PENDENTE DE CLASSIFICAÇÃO']
const CLASS_LABELS_EN = ['GOLD','SILVER','BRONZE','PENDING']

// Mapeamento PT→EN para enviar valores consistentes à API
const PURPOSE_PT_TO_EN = {
  'Observação da Terra': 'Earth Observation',
  'Desenvolvimento de Tecnologia': 'Technology Development',
  'Comunicações': 'Communications',
  'Ciências da Terra': 'Earth Science',
  'Ciências Espaciais': 'Space Science',
  'Ciências Espaciais/Demonstração Tecnológica': 'Space Science/Technology Demonstration',
  'Comunicações/Desenvolvimento de Tecnologia': 'Communications/Technology Development',
  'Comunicações/Rastreamento Marítimo': 'Communications/Maritime Tracking',
  'Demonstração Tecnológica': 'Technology Demonstration',
  'Navegação/Posicionamento Global': 'Navigation/Global Positioning',
  'Observação da Terra/Desenvolvimento de Tecnologia': 'Earth Observation/Technology Development',
  'Observação da Terra/Comunicações': 'Earth Observation/Communications',
  'Observação da Terra/Espaço': 'Earth/Space Observation',
  'Educacional': 'Educational',
  'Observação da Terra/Ciências da Terra': 'Earth Observation/Earth Science',
  'Plataforma': 'Platform',
  'Observação da Terra/Ciências Espaciais': 'Earth Observation/Space Science',
  'Observação da Terra/Navegação': 'Earth Observation/Navigation',
  'Comunicações/Navegação': 'Communications/Navigation',
  'Observação Espacial': 'Space Observation',
  'Vigilância': 'Surveillance',
  'Navegação/Posicionamento Regional': 'Navigation/Regional Positioning',
  'Ciências Espaciais/Desenvolvimento de Tecnologia': 'Space Science/Technology Development',
  'Tecnologia de Extensão de Missão': 'Mission Extension Technology',
  'Ciências da Terra/Observação da Terra': 'Earth Science/Earth Observation',
  'Observação da Terra/Comunicações/Ciências Espaciais': 'Earth Observation/Communications/Space Science',
  'Meteorológico': 'Meteorological',
  'Desenvolvimento de Tecnologia/Educacional': 'Technology Development/Educational',
  'Posicionamento por Satélite': 'Satellite Positioning',
  'Outro': 'Other'
}



// Comprehensive list of sovereign states (English names)
const COUNTRIES = [
  'Afghanistan','Albania','Algeria','Andorra','Angola','Antigua and Barbuda','Argentina','Armenia','Australia','Austria','Azerbaijan',
  'Bahamas','Bahrain','Bangladesh','Barbados','Belarus','Belgium','Belize','Benin','Bhutan','Bolivia','Bosnia and Herzegovina','Botswana','Brazil','Brunei','Bulgaria','Burkina Faso','Burundi',
  'Cabo Verde','Cambodia','Cameroon','Canada','Central African Republic','Chad','Chile','China','Colombia','Comoros','Congo','Costa Rica','Cote d\'Ivoire','Croatia','Cuba','Cyprus','Czechia',
  'Democratic Republic of the Congo','Denmark','Djibouti','Dominica','Dominican Republic',
  'Ecuador','Egypt','El Salvador','Equatorial Guinea','Eritrea','Estonia','Eswatini','Ethiopia',
  'Fiji','Finland','France','Gabon','Gambia','Georgia','Germany','Ghana','Greece','Grenada','Guatemala','Guinea','Guinea-Bissau','Guyana',
  'Haiti','Honduras','Hungary',
  'Iceland','India','Indonesia','Iran','Iraq','Ireland','Israel','Italy',
  'Jamaica','Japan','Jordan',
  'Kazakhstan','Kenya','Kiribati','Kuwait','Kyrgyzstan',
  'Laos','Latvia','Lebanon','Lesotho','Liberia','Libya','Liechtenstein','Lithuania','Luxembourg',
  'Madagascar','Malawi','Malaysia','Maldives','Mali','Malta','Marshall Islands','Mauritania','Mauritius','Mexico','Micronesia','Moldova','Monaco','Mongolia','Montenegro','Morocco','Mozambique','Myanmar',
  'Namibia','Nauru','Nepal','Netherlands','New Zealand','Nicaragua','Niger','Nigeria','North Korea','North Macedonia','Norway',
  'Oman',
  'Pakistan','Palau','Panama','Papua New Guinea','Paraguay','Peru','Philippines','Poland','Portugal',
  'Qatar',
  'Romania','Russia','Rwanda',
  'Saint Kitts and Nevis','Saint Lucia','Saint Vincent and the Grenadines','Samoa','San Marino','Sao Tome and Principe','Saudi Arabia','Senegal','Serbia','Seychelles','Sierra Leone','Singapore','Slovakia','Slovenia','Solomon Islands','Somalia','South Africa','South Korea','South Sudan','Spain','Sri Lanka','Sudan','Suriname','Sweden','Switzerland','Syria',
  'Taiwan','Tajikistan','Tanzania','Thailand','Timor-Leste','Togo','Tonga','Trinidad and Tobago','Tunisia','Turkey','Turkmenistan','Tuvalu',
  'Uganda','Ukraine','United Arab Emirates','United Kingdom','United States','Uruguay','Uzbekistan',
  'Vanuatu','Vatican City','Venezuela','Vietnam',
  'Yemen',
  'Zambia','Zimbabwe'
]

export default function App(){
  const [lang, setLang] = useState('en')
  const t = useMemo(()=> I18N[lang], [lang])
  const [form, setForm] = useState({ name:'', cnpj:'', address:'', email:'', sector:'', country:'', purpose:'', purposeOther:'', classification:'', delivery:'API', description:'' })
  const [rows, setRows] = useState([])
  const [selectedSatellites, setSelectedSatellites] = useState([])
  const [loading, setLoading] = useState(false)

  const onChange = (k)=>(e)=> setForm(s=>({...s, [k]: e.target.value}))

  const toggleSatellite = (satellite) => {
    setSelectedSatellites(prev => {
      const isSelected = prev.some(s => s.name_of_satellite === satellite.name_of_satellite)
      if (isSelected) {
        return prev.filter(s => s.name_of_satellite !== satellite.name_of_satellite)
      } else {
        return [...prev, satellite]
      }
    })
  }

  async function filter(){
    setLoading(true)
    try {
      const params = new URLSearchParams()
      const otherLabel = I18N[lang].other_label || 'Other'
      let effectivePurpose = form.purpose === otherLabel ? form.purposeOther : form.purpose
      
      // Converter PT→EN para a API (apenas purpose, classification já está em PT no banco)
      if (lang === 'pt' && effectivePurpose && PURPOSE_PT_TO_EN[effectivePurpose]) {
        effectivePurpose = PURPOSE_PT_TO_EN[effectivePurpose]
      }
      
      if(form.classification) params.set('classification', form.classification)
      if(effectivePurpose) params.set('purpose', effectivePurpose)
      if(form.delivery) params.set('delivery', form.delivery)
      params.set('limit','24')
      const res = await fetch(`${API}/satellites?${params.toString()}`)
      const data = await res.json()
      setRows(data)
      setSelectedSatellites([]) // Clear selection when filtering
    } catch (err) {
      console.error('Filter error:', err)
      setRows([])
    } finally {
      setLoading(false)
    }
  }

  async function submit(){
    const otherLabel = I18N[lang].other_label || 'Other'
    let effectivePurpose = form.purpose === otherLabel ? form.purposeOther : form.purpose
    
    // Converter PT→EN para a API (apenas purpose, classification já está em PT no banco)
    if (lang === 'pt' && effectivePurpose && PURPOSE_PT_TO_EN[effectivePurpose]) {
      effectivePurpose = PURPOSE_PT_TO_EN[effectivePurpose]
    }
    
    const payload = { 
      ...form, 
      purpose: effectivePurpose, 
      classification: form.classification || null, 
      language: lang,
      selected_satellites: selectedSatellites
    }
    try {
      const res = await fetch(`${API}/portal/request`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) })
      if(res.ok){ 
        const successMsg = lang === 'pt' 
          ? 'Sua solicitação foi enviada e será processada. Você receberá mais informações diretamente no e-mail cadastrado.'
          : 'Your request has been sent and will be processed. You will receive more information directly at the registered email.'
        alert(successMsg)
        setForm({ name:'', cnpj:'', address:'', email:'', sector:'', country:'', purpose:'', purposeOther:'', classification:'', delivery:'API', description:'' })
        setSelectedSatellites([])
        setRows([])
      } else {
        const errorData = await res.json()
        console.error('Error submitting request:', errorData)
        alert(lang === 'pt' ? 'Erro ao enviar solicitação. Verifique os dados.' : 'Error submitting request. Please check your data.')
      }
    } catch (error) {
      console.error('Network error:', error)
      alert(lang === 'pt' ? 'Erro de conexão com o servidor.' : 'Server connection error.')
    }
  }

  return (
    <>
      <canvas id="space" className="space" aria-hidden="true"></canvas>
      <div className="grid-overlay" aria-hidden="true"></div>

      <nav aria-label="Main">
        <div className="container nav-inner">
          <a href="/" className="logo" aria-label="OrbitHub">
            <img
              src="/logo.png"
              alt="OrbitHub"
              className="logo-img"
            />
          </a>
          <div className="nav-links">
            <div className="lang-switch" role="group" aria-label="Language">
              <button className={`lang ${lang==='en'?'active':''}`} aria-pressed={lang==='en'} onClick={()=>{document.documentElement.lang='en';setLang('en')}}>EN</button>
              <button className={`lang ${lang==='pt'?'active':''}`} aria-pressed={lang==='pt'} onClick={()=>{document.documentElement.lang='pt-BR';setLang('pt')}}>PT</button>
            </div>
            <a className="btn-ghost" href="/">{t.home}</a>
            <a className="cta" href="#request" style={{color:'#000'}}>{t.nav_cta}</a>
          </div>
        </div>
      </nav>

      <header className="container hero" id="topo">
        <div>
          <span className="badge">{t.badge}</span>
          <h1 dangerouslySetInnerHTML={{__html: t.hero_title}} />
          <p className="sub">{t.hero_sub}</p>
          <div style={{display:'flex',gap:10,marginTop:12,flexWrap:'wrap'}}>
            <span className="chip">{t.chip_carbon}</span>
            <span className="chip" style={{background:'rgba(138,43,226,.14)', color:'#c9a7ff'}}>{t.chip_sats}</span>
            <span className="chip" style={{background:'rgba(0,209,255,.14)', color:'#9be8ff'}}>{t.chip_samples}</span>
          </div>
        </div>
        <div aria-hidden="true" className="globe-wrap">
          <div className="globe-grid"></div>
          <div className="globe-line"></div>
          <div className="globe-line" style={{'--r': '30deg'}}></div>
          <div className="globe-line" style={{'--r': '60deg'}}></div>
          <div className="globe-line" style={{'--r': '90deg'}}></div>
        </div>
      </header>

      <main>
        <section id="request" className="container section">
          <div className="kicker">{t.portal_kicker}</div>
          <h2 className="title">{t.portal_title}</h2>
          <p style={{textAlign:'center', marginTop:'0.5rem', marginBottom:'2rem', color:'rgba(255,255,255,0.7)', fontSize:'1rem'}}>
            {t.portal_instructions}
          </p>
          <div className="cards">
            <div className="card" style={{gridColumn:'span 6'}}>
              <h3>{t.client_title}</h3>
              <div className="row">
                <div style={{gridColumn:'span 6'}}><label>{t.name} <span className="info" title={t.name_hint}>!</span></label><input value={form.name} onChange={onChange('name')} placeholder={t.name} /></div>
                <div style={{gridColumn:'span 6'}}><label>{t.cnpj} <span className="info" title={t.cnpj_hint}>!</span></label><input value={form.cnpj} onChange={onChange('cnpj')} placeholder={t.cnpj} /></div>
                <div style={{gridColumn:'span 12'}}><label>{t.address} <span className="info" title={t.address_hint}>!</span></label><input value={form.address} onChange={onChange('address')} placeholder={t.address} /></div>
                <div style={{gridColumn:'span 6'}}><label>{t.email} <span className="info" title={t.email_hint}>!</span></label><input type="email" value={form.email} onChange={onChange('email')} placeholder={t.email} /></div>
                <div style={{gridColumn:'span 6'}}>
                  <label>{t.sector} <span className="info" title={t.sector_hint}>!</span></label>
                  <select value={form.sector} onChange={onChange('sector')}>
                    <option value="">--</option>
                    {[...t.sector_options].sort((a,b)=>a.localeCompare(b, lang==='pt'?'pt-BR':'en', {sensitivity:'base'})).map(s => (
                      <option key={s} value={s}>{s}</option>
                    ))}
                  </select>
                </div>
                <div style={{gridColumn:'span 12'}}>
                  <label>{t.country} <span className="info" title={t.country_hint}>!</span></label>
                  <select value={form.country} onChange={onChange('country')}>
                    <option value="">--</option>
                    {COUNTRIES
                      .sort((a,b)=>a.localeCompare(b))
                      .map(c => (<option key={c} value={c}>{c}</option>))}
                  </select>
                </div>
              </div>
            </div>
            <div className="card" style={{gridColumn:'span 6'}}>
              <h3>{t.request_title}</h3>
              <div className="row">
                <div style={{gridColumn:'span 6'}}><label>{t.purpose} <span className="info" title={t.purpose_hint}>!</span></label>
                  <select value={form.purpose} onChange={onChange('purpose')}>
                    <option value="">--</option>
                    {[...t.purpose_options]
                      .sort((a,b)=>a.localeCompare(b, lang==='pt'?'pt-BR':'en', {sensitivity:'base'}))
                      .map(opt => (
                        <option key={opt} value={opt}>{opt}</option>
                      ))}
                  </select>
                  {/* extra input handled below as full-width */}
                </div>
                {form.purpose === (I18N[lang].other_label || 'Other') && (
                  <div style={{gridColumn:'span 12', marginTop:8}}>
                    <label>{I18N[lang].specify_other} <span className="info" title={I18N[lang].other_hint}>!</span></label>
                    <textarea style={{minHeight:80}} value={form.purposeOther} onChange={onChange('purposeOther')} placeholder={I18N[lang].other_placeholder}></textarea>
                  </div>
                )}
                <div style={{gridColumn:'span 6'}}><label>{t.classification} <span className="info" title={t.classification_hint} aria-label="info">!</span></label>
                  <select value={form.classification} onChange={onChange('classification')}>
                    <option value="">--</option>
                    {CLASS_VALUES.map((val, idx) => (
                      <option key={val} value={val}>{(lang==='pt' ? CLASS_LABELS_PT : CLASS_LABELS_EN)[idx]}</option>
                    ))}
                  </select>
                </div>
                <div style={{gridColumn:'span 6'}}><label>{t.delivery} <span className="info" title={t.delivery_hint}>!</span></label>
                  <select value={form.delivery} onChange={onChange('delivery')}>
                    <option value="API">API</option>
                    <option value="Batch">Batch</option>
                  </select>
                </div>
                <div style={{gridColumn:'span 12'}}><label>{t.description} <span className="info" title={t.description_hint}>!</span></label><textarea value={form.description} onChange={onChange('description')} placeholder={t.description}></textarea></div>
              </div>
              <div style={{display:'flex', gap:10, marginTop:12}}>
                <button className="btn-ghost" onClick={filter} disabled={loading}>🔎 {t.filter_btn}</button>
                <button className="btn" onClick={submit}>🚀 {t.submit_btn}</button>
              </div>
            </div>
            <div className="card" style={{gridColumn:'span 12'}}>
              <h3>{t.satellites} {selectedSatellites.length > 0 && <span style={{color:'var(--primary)', fontSize:'0.9em'}}>({selectedSatellites.length} {lang === 'pt' ? 'selecionado(s)' : 'selected'})</span>}</h3>
              {loading && (
                <div className="progress" role="progressbar" aria-label={lang==='pt'?'Carregando':'Loading'}>
                  <div className="progress-bar"></div>
                </div>
              )}
              <div className="list">
                {rows?.length? rows.map((r,i)=> {
                  const isSelected = selectedSatellites.some(s => s.name_of_satellite === r.name_of_satellite)
                  return (
                    <div key={i} className="item" style={{cursor:'pointer', border: isSelected ? '2px solid var(--primary)' : '1px solid rgba(0,209,255,0.2)', position:'relative'}} onClick={() => toggleSatellite(r)}>
                      <input 
                        type="checkbox" 
                        checked={isSelected} 
                        onChange={() => toggleSatellite(r)}
                        style={{position:'absolute', top:12, right:12, cursor:'pointer', width:18, height:18}}
                        onClick={(e) => e.stopPropagation()}
                      />
                      <h4>{r.name_of_satellite || r.OBJECT_NAME || 'Unknown satellite'}</h4>
                      {classBadge(r.sustainability_class || r.SUSTAINABILITY_CLASS, lang)}
                      <div style={{marginTop:6, color:'var(--muted)'}}>
                        {r.alternate_names && <div><strong>Alt:</strong> {r.alternate_names}</div>}
                        {r.country_un_registry && <div><strong>UN Registry:</strong> {r.country_un_registry}</div>}
                        {r.country_operator_owner && <div><strong>Country/Operator:</strong> {r.country_operator_owner}</div>}
                        {r.operator_owner && <div><strong>Owner:</strong> {r.operator_owner}</div>}
                        {r.purpose && <div><strong>Purpose:</strong> {r.purpose}</div>}
                        {r.detailed_purpose && <div><strong>Detailed:</strong> {r.detailed_purpose}</div>}
                      </div>
                    </div>
                  )
                }) : (loading ? <em>{t.loading}</em> : <em>{t.no_results}</em>)}
              </div>
            </div>
          </div>
        </section>
      </main>
    </>
  )
}


