document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    const stressInput = document.getElementById('stress');
    const stressBadge = document.getElementById('stressBadge');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');
    const resultBox = document.getElementById('resultBox');

    // Tab Switching Logic
    const navItems = document.querySelectorAll('.nav-item');
    const viewSections = document.querySelectorAll('.view-section');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = item.getAttribute('data-target');
            if (!targetId) return;

            // Remove active class from all tabs
            navItems.forEach(nav => nav.classList.remove('active'));
            // Add active class to clicked tab
            item.classList.add('active');

            // Hide all views
            viewSections.forEach(view => view.classList.remove('active-view'));
            // Show target view
            document.getElementById(targetId).classList.add('active-view');
        });
    });

    // Start Assessment Button Logic
    const startAssessmentBtn = document.getElementById('startAssessmentBtn');
    if (startAssessmentBtn) {
        startAssessmentBtn.addEventListener('click', () => {
            const assessmentTab = document.querySelector('.nav-item[data-target="view-assessment"]');
            if (assessmentTab) {
                assessmentTab.click();
            }
        });
    }

    // BMI Calculator Logic
    const calcBmiBtn = document.getElementById('calcBmiBtn');
    if (calcBmiBtn) {
        calcBmiBtn.addEventListener('click', () => {
            const weight = parseFloat(document.getElementById('quickWeight').value);
            const heightCm = parseFloat(document.getElementById('quickHeight').value);
            const bmiValDisplay = document.getElementById('bmiVal');
            const bmiLabelDisplay = document.getElementById('bmiLabel');
            
            if (weight > 0 && heightCm > 0) {
                const heightM = heightCm / 100;
                const bmi = (weight / (heightM * heightM)).toFixed(1);
                bmiValDisplay.textContent = bmi;
                
                let category = '';
                let color = '';
                if (bmi < 18.5) { category = 'Underweight'; color = '#F59E0B'; }
                else if (bmi < 25) { category = 'Normal'; color = '#10B981'; }
                else if (bmi < 30) { category = 'Overweight'; color = '#F59E0B'; }
                else { category = 'Obese'; color = '#EF4444'; }
                
                bmiLabelDisplay.textContent = category;
                bmiValDisplay.style.color = color;
            } else {
                bmiValDisplay.textContent = '--';
                bmiLabelDisplay.textContent = 'Invalid input';
                bmiValDisplay.style.color = 'white';
            }
        });
    }

    // Update stress value display dynamically (move slider badge)
    stressInput.addEventListener('input', (e) => {
        stressBadge.textContent = e.target.value;
        const val = (e.target.value - e.target.min) / (e.target.max - e.target.min);
        const thumbOffset = 8; // Half thumb width approx
        stressBadge.style.left = `calc(${val * 100}% + ${0.5 - val} * ${thumbOffset * 2}px)`;
    });
    // Trigger initial positioning
    stressInput.dispatchEvent(new Event('input'));

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        btnText.style.display = 'none';
        loader.style.display = 'block';
        submitBtn.disabled = true;

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                renderResult(result.risk, result.confidence);
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error(error);
            alert('Failed to connect to the server.');
        } finally {
            btnText.style.display = 'inline-block';
            loader.style.display = 'none';
            submitBtn.disabled = false;
        }
    });

    function renderResult(risk, confidence) {
        let color = '';
        let msg = '';
        let icon = '';
        
        if (risk === 'Low Risk') {
            color = '#10B981';
            msg = 'Congratulations! Your health profile is considered low risk.';
            icon = 'fa-shield-check';
        } else if (risk === 'Prediabetes') {
            color = '#F59E0B';
            msg = 'Your profile suggests you may be in the prediabetes stage. Early lifestyle changes are recommended.';
            icon = 'fa-triangle-exclamation';
        } else {
            color = '#EF4444';
            msg = 'Your profile indicates a high risk. Please consult a healthcare professional for diagnosis.';
            icon = 'fa-circle-exclamation';
        }

        let riskScore = 0;
        if (risk === 'Low Risk') riskScore = Math.floor(Math.random() * 20) + 5;
        if (risk === 'Prediabetes') riskScore = Math.floor(Math.random() * 25) + 40;
        if (risk === 'High Risk') riskScore = Math.floor(Math.random() * 20) + 75;

        let healthScore = 100 - riskScore + Math.floor(Math.random() * 10 - 5);
        if (healthScore > 100) healthScore = 100;

        // Semi-circle Math: stroke-dasharray is circumference (2 * pi * r).
        // For r=40, C=251.2. A semicircle is 125.6.
        // We set dasharray to 125.6 and offset from 125.6 down to 0.
        let arcLength = 125.6; 
        let riskOffset = arcLength - (arcLength * (riskScore / 100));
        let confOffset = arcLength - (arcLength * (confidence / 100)); // for confidence mini gauge (r=10 -> C=62.8 -> half=31.4)
        
        let avgRisk = (risk === 'Low Risk') ? 15 : (risk === 'Prediabetes' ? 45 : 85);

        let html = `
            <div class="risk-header-banner" style="border-color: ${color}40; background: ${color}10;">
                <div class="risk-title" style="color: ${color};">
                    <i class="fa-solid fa-circle-check"></i> DIABETES RISK: ${risk.toUpperCase().split(' ')[0]}
                </div>
                <div class="risk-desc">${msg}</div>
            </div>

            <div class="gauge-and-benchmark">
                <div class="gauge-container">
                    <div class="semi-gauge">
                        <svg viewBox="0 0 100 100">
                            <!-- SVG centers at 50,50, radius 40. Semicircle goes from right to left because of rotate(180deg) -->
                            <circle cx="50" cy="50" r="40" class="gauge-bg" stroke-dasharray="125.6 251.2" stroke-dashoffset="0"></circle>
                            <circle cx="50" cy="50" r="40" class="gauge-val" style="stroke: ${color};" stroke-dasharray="125.6 251.2" stroke-dashoffset="125.6"></circle>
                        </svg>
                    </div>
                    <div class="gauge-text">
                        <h3>${riskScore}%</h3>
                        <span>Risk Score</span>
                    </div>
                    <div class="gauge-labels">
                        <span>0%</span>
                        <span>100%</span>
                    </div>
                </div>

                <div class="benchmarks">
                    <span>Risk Benchmarks</span>
                    <div class="bars-container">
                        <div class="bar-group">
                            <span class="bar-val">${riskScore}%</span>
                            <div class="bar" style="height: 0%; background: ${color};" data-target="${riskScore}"></div>
                            <span class="bar-label">Your Risk</span>
                        </div>
                        <div class="bar-group" style="margin-left: 2rem;">
                            <span class="bar-val">${avgRisk}%</span>
                            <div class="bar" style="height: 0%; background: var(--border-color);" data-target="${avgRisk}"></div>
                            <span class="bar-label">Average Risk</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-box">
                    <span>Risk Level</span>
                    <strong style="color: ${color}; display:flex; align-items:center; gap:4px;">
                        <span style="width:8px;height:8px;border-radius:50%;background:${color};display:inline-block;"></span>
                        ${risk.split(' ')[0]}
                    </strong>
                </div>
                <div class="stat-box">
                    <span>Confidence</span>
                    <div style="display:flex; align-items:center; gap:0.5rem; flex-direction:column;">
                        <strong style="color: #38BDF8;">${confidence}%</strong>
                        <div class="confidence-svg">
                            <svg viewBox="0 0 24 24">
                                <circle cx="12" cy="12" r="10" class="conf-bg" stroke-dasharray="31.4 62.8" stroke-dashoffset="0"></circle>
                                <circle cx="12" cy="12" r="10" class="conf-val" style="stroke: ${color};" stroke-dasharray="31.4 62.8" stroke-dashoffset="31.4"></circle>
                            </svg>
                        </div>
                    </div>
                </div>
                <div class="stat-box">
                    <span>Health Score</span>
                    <strong style="color: #A855F7;">${healthScore} / 100</strong>
                </div>
                <div class="stat-box">
                    <span>Model Type</span>
                    <strong style="color: #F59E0B;">AI / ML</strong>
                </div>
            </div>

            <div class="rec-title"><i class="fa-solid fa-person-running" style="color: #38BDF8;"></i> Personalized Prevention Steps</div>
            <div class="rec-grid">
                ${getRecommendationsGrid(risk)}
            </div>

            <div class="disclaimer">
                <i class="fa-solid fa-circle-info"></i>
                <div>This is an AI-generated assessment and not a substitute for professional medical advice. Consult a healthcare professional for diagnosis.</div>
            </div>
        `;

        resultBox.innerHTML = html;
        
        // Trigger animations
        setTimeout(() => {
            const gauge = resultBox.querySelector('.gauge-val');
            if(gauge) gauge.style.strokeDashoffset = riskOffset;

            const confGauge = resultBox.querySelector('.conf-val');
            // C = 62.8, half = 31.4
            let confValOffset = 31.4 - (31.4 * (confidence / 100));
            if(confGauge) confGauge.style.strokeDashoffset = confValOffset;

            const bars = resultBox.querySelectorAll('.bar');
            bars.forEach(bar => {
                bar.style.height = bar.getAttribute('data-target') + '%';
            });
        }, 100);

        resultBox.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function getRecommendationsGrid(risk) {
        if (risk === 'Low Risk') {
            return `
                <div class="rec-card">
                    <div class="rec-card-header">
                        <div class="rec-icon" style="background: #10B981;"><i class="fa-solid fa-leaf"></i></div>
                        <strong>Maintain Diet</strong>
                    </div>
                    <p>Eat balanced meals with low sugar and high fiber. Expanded tips available in Health Tips section.</p>
                </div>
                <div class="rec-card">
                    <div class="rec-card-header">
                        <div class="rec-icon" style="background: #38BDF8;"><i class="fa-solid fa-person-running"></i></div>
                        <strong>Stay Active</strong>
                    </div>
                    <p>Exercise for at least 30 minutes daily to maintain insulin sensitivity and cardiovascular health.</p>
                </div>
                <div class="rec-card">
                    <div class="rec-card-header">
                        <div class="rec-icon" style="background: #8B5CF6;"><i class="fa-solid fa-droplet"></i></div>
                        <strong>Stay Hydrated</strong>
                    </div>
                    <p>Drink plenty of water for health throughout the day to support kidney function.</p>
                </div>
                <div class="rec-card">
                    <div class="rec-card-header">
                        <div class="rec-icon" style="background: #F59E0B;"><i class="fa-regular fa-calendar-check"></i></div>
                        <strong>Regular Checkups</strong>
                    </div>
                    <p>Schedule routine health checkups to monitor your vitals proactively.</p>
                </div>
            `;
        } else if (risk === 'Prediabetes') {
            return `
                <div class="rec-card">
                    <div class="rec-card-header">
                        <div class="rec-icon" style="background: #EF4444;"><i class="fa-solid fa-ban"></i></div>
                        <strong>Reduce Sugar</strong>
                    </div>
                    <p>Cut down on sugary foods and refined carbs to prevent blood sugar spikes.</p>
                </div>
                <div class="rec-card">
                    <div class="rec-card-header">
                        <div class="rec-icon" style="background: #38BDF8;"><i class="fa-solid fa-dumbbell"></i></div>
                        <strong>Increase Exercise</strong>
                    </div>
                    <p>Aim for 150 minutes of moderate activity per week to improve glucose uptake.</p>
                </div>
                <div class="rec-card">
                    <div class="rec-card-header">
                        <div class="rec-icon" style="background: #8B5CF6;"><i class="fa-solid fa-scale-balanced"></i></div>
                        <strong>Weight Management</strong>
                    </div>
                    <p>Work towards and maintain a healthy BMI through diet and exercise.</p>
                </div>
                <div class="rec-card">
                    <div class="rec-card-header">
                        <div class="rec-icon" style="background: #F59E0B;"><i class="fa-solid fa-bed"></i></div>
                        <strong>Improve Sleep</strong>
                    </div>
                    <p>Ensure 7-8 hours of quality sleep to regulate stress hormones.</p>
                </div>
            `;
        } else {
            return `
                <div class="rec-card">
                    <div class="rec-card-header">
                        <div class="rec-icon" style="background: #EF4444;"><i class="fa-solid fa-user-doctor"></i></div>
                        <strong>Consult Doctor</strong>
                    </div>
                    <p>Please consult a doctor as soon as possible for a professional diagnosis.</p>
                </div>
                <div class="rec-card">
                    <div class="rec-card-header">
                        <div class="rec-icon" style="background: #F59E0B;"><i class="fa-solid fa-vial"></i></div>
                        <strong>Get Lab Tests</strong>
                    </div>
                    <p>Perform diagnostic tests like Fasting Blood Sugar and HbA1c as prescribed.</p>
                </div>
                <div class="rec-card">
                    <div class="rec-card-header">
                        <div class="rec-icon" style="background: #10B981;"><i class="fa-solid fa-bowl-food"></i></div>
                        <strong>Strict Diet</strong>
                    </div>
                    <p>Begin a diabetes-friendly diet immediately under medical guidance.</p>
                </div>
                <div class="rec-card">
                    <div class="rec-card-header">
                        <div class="rec-icon" style="background: #38BDF8;"><i class="fa-solid fa-pills"></i></div>
                        <strong>Medication</strong>
                    </div>
                    <p>Follow prescribed medications and treatment plans diligently.</p>
                </div>
            `;
        }
    }
});
