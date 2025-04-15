import { useState } from 'react';

const DEFAULT_EXCHANGE_RATE = 24.44; // CHF to MXN

// Mock housing data based on your dataset
const housingData = [
  { id: 1, location: "Avenue de Valmont 20", price: 2560, size: 124, type: "Apartment", pricePerSqm: 20.65, travelTime: 30 },
  { id: 2, location: "d'Echallens 8", price: 2276, size: 85, type: "Apartment", pricePerSqm: 26.78, travelTime: 25 },
  { id: 3, location: "Avenue de la Chablière 35bis", price: 2060, size: 78, type: "Apartment", pricePerSqm: 26.41, travelTime: 30 },
  { id: 4, location: "Route du Pavement 34", price: 2750, size: 100, type: "Apartment", pricePerSqm: 27.50, travelTime: 35 },
  { id: 5, location: "Rue Couchirard 4", price: 2790, size: 102, type: "Apartment", pricePerSqm: 27.35, travelTime: 30 },
  { id: 6, location: "Avenue Virgile-Rossel 9", price: 2860, size: 100, type: "Apartment", pricePerSqm: 28.60, travelTime: 30 },
  { id: 7, location: "Violette District 4", price: 3350, size: 120, type: "Apartment", pricePerSqm: 27.92, travelTime: 35 },
  { id: 8, location: "Avenue du Grey 76", price: 1790, size: 103, type: "Apartment", pricePerSqm: 17.38, travelTime: 35 },
];

// Predefined monthly budget for two people
const defaultBudget = {
  housing: 3000,
  utilities: 750,
  groceries: 1000,
  transportation: 300,
  healthcare: 1200,
  education: 300,
  entertainment: 400,
  other: 500
};

const Dashboard = () => {
  const [selectedHousing, setSelectedHousing] = useState(null);
  const [budget, setBudget] = useState(defaultBudget);
  const [showBudgetEditor, setShowBudgetEditor] = useState(false);
  const [exchangeRate, setExchangeRate] = useState(DEFAULT_EXCHANGE_RATE);
  const [currency, setCurrency] = useState('CHF');
  
  // Calculate budget impact
  const calculateBudgetImpact = (housingPrice) => {
    const difference = housingPrice - budget.housing;
    return difference;
  };
  
  // Calculate total budget
  const totalBudget = Object.values(budget).reduce((sum, value) => sum + value, 0);
  
  // Apply currency conversion
  const convertCurrency = (amount) => {
    if (currency === 'MXN') {
      return (amount * exchangeRate).toFixed(0);
    }
    return amount;
  };
  
  // Format currency
  const formatCurrency = (amount) => {
    return `${currency === 'CHF' ? 'CHF' : 'MXN'} ${convertCurrency(amount).toLocaleString()}`;
  };
  
  return (
    <div className="bg-gray-100 min-h-screen p-4">
      <div className="max-w-6xl mx-auto">
        <header className="mb-6">
          <h1 className="text-3xl font-bold text-blue-800">Lausanne Housing &amp; Budget Dashboard</h1>
          <p className="text-gray-600">Plan your EPFL move with our interactive tools</p>
        </header>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Left column - Housing options */}
          <div className="md:col-span-2">
            <div className="bg-white rounded-lg shadow p-4 mb-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold">Housing Options</h2>
                <div className="flex items-center">
                  <select 
                    className="border rounded p-1 mr-2"
                    value={currency}
                    onChange={(e) => setCurrency(e.target.value)}
                  >
                    <option value="CHF">CHF</option>
                    <option value="MXN">MXN</option>
                  </select>
                  {currency === 'MXN' && (
                    <input 
                      type="number" 
                      className="border rounded p-1 w-20"
                      value={exchangeRate}
                      onChange={(e) => setExchangeRate(parseFloat(e.target.value))}
                      min="1"
                      step="0.01"
                    />
                  )}
                </div>
              </div>
              
              <div className="overflow-auto">
                <table className="min-w-full">
                  <thead>
                    <tr className="bg-gray-100">
                      <th className="py-2 px-3 text-left">Location</th>
                      <th className="py-2 px-3 text-right">Price</th>
                      <th className="py-2 px-3 text-right">Size (m²)</th>
                      <th className="py-2 px-3 text-right">CHF/m²</th>
                      <th className="py-2 px-3 text-right">Time to EPFL</th>
                      <th className="py-2 px-3 text-right">Budget Impact</th>
                      <th className="py-2 px-3"></th>
                    </tr>
                  </thead>
                  <tbody>
                    {housingData.map((housing) => (
                      <tr 
                        key={housing.id} 
                        className={`border-b hover:bg-blue-50 ${selectedHousing?.id === housing.id ? 'bg-blue-100' : ''}`}
                      >
                        <td className="py-2 px-3">{housing.location}</td>
                        <td className="py-2 px-3 text-right">
                          {formatCurrency(housing.price)}
                        </td>
                        <td className="py-2 px-3 text-right">{housing.size}</td>
                        <td className="py-2 px-3 text-right">{housing.pricePerSqm.toFixed(2)}</td>
                        <td className="py-2 px-3 text-right">{housing.travelTime} min</td>
                        <td className="py-2 px-3 text-right">
                          <span className={calculateBudgetImpact(housing.price) > 0 ? 'text-red-600' : 'text-green-600'}>
                            {calculateBudgetImpact(housing.price) > 0 ? '+' : ''}
                            {formatCurrency(calculateBudgetImpact(housing.price))}
                          </span>
                        </td>
                        <td className="py-2 px-3">
                          <button 
                            className="bg-blue-500 text-white px-2 py-1 rounded text-sm"
                            onClick={() => setSelectedHousing(housing)}
                          >
                            Select
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
            
            {/* Housing comparison visualization */}
            <div className="bg-white rounded-lg shadow p-4">
              <h2 className="text-xl font-bold mb-4">Housing Comparison</h2>
              
              <div className="h-64 flex items-end space-x-2">
                {housingData.map((housing) => (
                  <div key={housing.id} className="flex flex-col items-center">
                    <div 
                      className={`w-12 transition-all ${
                        selectedHousing?.id === housing.id 
                          ? 'bg-blue-600' 
                          : 'bg-blue-400 hover:bg-blue-500'
                      }`}
                      style={{ 
                        height: `${(housing.price / 6000) * 200}px`,
                        cursor: 'pointer'
                      }}
                      onClick={() => setSelectedHousing(housing)}
                    ></div>
                    <div className="text-xs mt-1 w-16 text-center overflow-hidden text-ellipsis whitespace-nowrap" title={housing.location}>
                      {housing.location.split(' ')[0]}
                    </div>
                    <div className="text-xs font-bold">{currency === 'CHF' ? 'CHF' : 'MXN'} {convertCurrency(housing.price)}</div>
                  </div>
                ))}
                
                {/* Budget line */}
                <div className="absolute left-0 right-0 border-t-2 border-red-500 border-dashed" style={{ 
                  bottom: `${(budget.housing / 6000) * 200 + 16}px`, 
                  marginLeft: '1rem',
                  marginRight: '1rem'
                }}>
                  <span className="bg-white text-red-500 text-xs px-1 absolute -top-3">Budget: {formatCurrency(budget.housing)}</span>
                </div>
              </div>
            </div>
          </div>
          
          {/* Right column - Budget */}
          <div>
            <div className="bg-white rounded-lg shadow p-4 mb-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold">Monthly Budget</h2>
                <button 
                  className="bg-blue-500 text-white px-2 py-1 rounded text-sm"
                  onClick={() => setShowBudgetEditor(!showBudgetEditor)}
                >
                  {showBudgetEditor ? 'Done' : 'Edit'}
                </button>
              </div>
              
              {Object.entries(budget).map(([category, amount]) => (
                <div key={category} className="mb-3">
                  <div className="flex justify-between items-center mb-1">
                    <div className="capitalize">{category}</div>
                    <div className="font-bold">
                      {showBudgetEditor ? (
                        <input 
                          type="number" 
                          className="border rounded p-1 w-24 text-right"
                          value={amount}
                          onChange={(e) => setBudget({...budget, [category]: parseFloat(e.target.value)})}
                          min="0"
                          step="10"
                        />
                      ) : (
                        formatCurrency(amount)
                      )}
                    </div>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${(amount / totalBudget) * 100}%` }}
                    ></div>
                  </div>
                </div>
              ))}
              
              <div className="mt-4 pt-4 border-t">
                <div className="flex justify-between items-center">
                  <div className="font-bold">Total</div>
                  <div className="font-bold text-lg">{formatCurrency(totalBudget)}</div>
                </div>
              </div>
            </div>
            
            {/* Selected housing details */}
            {selectedHousing && (
              <div className="bg-white rounded-lg shadow p-4">
                <h2 className="text-xl font-bold mb-4">Selected Housing</h2>
                
                <div className="mb-3">
                  <div className="text-sm text-gray-600">Location</div>
                  <div className="font-bold">{selectedHousing.location}</div>
                </div>
                
                <div className="grid grid-cols-2 gap-4 mb-3">
                  <div>
                    <div className="text-sm text-gray-600">Price</div>
                    <div className="font-bold">{formatCurrency(selectedHousing.price)}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Size</div>
                    <div className="font-bold">{selectedHousing.size} m²</div>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4 mb-3">
                  <div>
                    <div className="text-sm text-gray-600">Price per m²</div>
                    <div className="font-bold">{currency === 'CHF' ? 'CHF' : 'MXN'} {convertCurrency(selectedHousing.pricePerSqm).toFixed(2)}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Travel Time</div>
                    <div className="font-bold">{selectedHousing.travelTime} min</div>
                  </div>
                </div>
                
                <div className="mt-4 pt-4 border-t">
                  <div className="text-sm text-gray-600">Budget Impact</div>
                  <div className={`font-bold text-lg ${calculateBudgetImpact(selectedHousing.price) > 0 ? 'text-red-600' : 'text-green-600'}`}>
                    {calculateBudgetImpact(selectedHousing.price) > 0 ? '+' : ''}
                    {formatCurrency(calculateBudgetImpact(selectedHousing.price))}
                  </div>
                  <div className="text-sm text-gray-600 mt-1">
                    {calculateBudgetImpact(selectedHousing.price) > 0 
                      ? 'Over housing budget' 
                      : 'Under housing budget'}
                  </div>
                  
                  <div className="mt-4">
                    <div className="text-sm text-gray-600">New Total Budget</div>
                    <div className="font-bold text-lg">
                      {formatCurrency(totalBudget - budget.housing + selectedHousing.price)}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;