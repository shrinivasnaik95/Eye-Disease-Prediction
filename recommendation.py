# =====================================================
# Recommendation based on medical condition for 8 classes
# =====================================================

amd = """**For AMD (Age-related Macular Degeneration)**:
- **Recommendation**:
    - **Immediate Referral**: Consult a retinal specialist for assessment and monitoring.
    - **Treatment Options**:
      - **Anti-VEGF Therapy**: For wet AMD, injections like Ranibizumab or Aflibercept can slow vision loss.
      - **Photodynamic Therapy (PDT)**: May be combined with anti-VEGF in some cases.
    - **Lifestyle and Monitoring**:
      - **Diet**: High in antioxidants, leafy greens, and omega-3 fatty acids.
      - **AREDS2 Supplements**: Recommended for patients at moderate or high risk of progression.
      - **Regular OCT Monitoring**: Follow-up every 6–12 months depending on severity.
    - **Next Steps**:
      - Schedule routine visits with your retina specialist.
      - Maintain healthy lifestyle habits to slow progression.
"""

cnv = """**For CNV (Choroidal Neovascularization)**:
- **Recommendation**: 
    - **Immediate Referral**: Seek prompt evaluation by a retinal specialist.
    - **Treatment Options**: 
      - **Anti-VEGF Therapy**: Injections such as Ranibizumab or Aflibercept.
      - **Photodynamic Therapy (PDT)**: May be combined with anti-VEGF treatment.
      - **Laser Therapy**: Used in select cases.
    - **Lifestyle and Monitoring**: 
      - **Diet**: Rich in leafy greens, omega-3 fatty acids, and antioxidants.
      - **Supplements**: AREDS2 formulation recommended for AMD-associated CNV.
      - **OCT Monitoring**: Every 1–3 months.
    - **Next Steps**: 
      - Follow-up with retina specialist and continue treatment as advised.
"""

csr = """**For CSR (Central Serous Retinopathy)**:
- **Recommendation**:
    - **Observation**: Many cases resolve spontaneously within 3–4 months.
    - **Treatment Options**:
      - **Photodynamic Therapy (PDT)**: Low-fluence PDT for chronic or recurrent cases.
      - **Laser Treatment**: Focal laser to leaking points if indicated.
    - **Lifestyle Modifications**:
      - **Stress Management**: Reduce stress, as CSR is often stress-related.
      - **Corticosteroid Avoidance**: Avoid systemic or topical steroids if possible.
    - **Monitoring**:
      - **OCT Follow-up**: Monitor subretinal fluid every 1–3 months.
      - **Visual Function**: Check for metamorphopsia and visual acuity changes.
    - **Next Steps**:
      - Schedule follow-up with retinal specialist.
      - Consider lifestyle adjustments and treatment if persistent or recurrent.
"""

dme = '''**For DME (Diabetic Macular Edema)**:
- **Recommendation**:
    - **Endocrinology Consultation**: Coordinate with endocrinologist to control systemic diabetes.
    - **Treatment Options**: 
      - **Anti-VEGF Injections**: First-line therapy for retinal swelling.
      - **Corticosteroid Implants**: Used if anti-VEGF is insufficient.
      - **Laser Photocoagulation**: Treat localized leakage areas.
    - **Blood Sugar and Blood Pressure Control**: 
      - Maintain HbA1c <7% and BP <140/80 mmHg.
    - **Monitoring**:
      - **OCT Exams**: Every 3–6 months.
      - **Diabetes Management**: Tight glycemic control to prevent recurrence.
    - **Next Steps**:
      - Visit retina specialist and endocrinologist.
      - Continue anti-VEGF therapy as required.
'''

dr = '''**For DR (Diabetic Retinopathy)**:
- **Recommendation**:
    - **Immediate Referral**: Retinal specialist evaluation is essential.
    - **Treatment Options**:
      - **Laser Photocoagulation**: For proliferative DR to prevent vision loss.
      - **Anti-VEGF Therapy**: In case of macular edema or neovascularization.
      - **Vitrectomy**: If vitreous hemorrhage or tractional retinal detachment occurs.
    - **Systemic Control**:
      - **Blood Sugar Management**: HbA1c <7%.
      - **Blood Pressure & Cholesterol**: Keep within target ranges.
    - **Monitoring**:
      - **OCT & Fundus Exams**: Every 3–6 months depending on severity.
    - **Next Steps**:
      - Regular follow-ups with retina specialist.
      - Maintain systemic health to slow disease progression.
'''

drusen = '''**For Drusen (Early AMD)**:
- **Recommendation**:
    - **Dietary Changes**:
      - High in antioxidants (vitamins C, E, zinc, copper, beta-carotene).
      - Include leafy greens, kale, and fish rich in omega-3.
      - **AREDS2 Supplements** for moderate/high risk.
    - **Lifestyle Modifications**:
      - Quit smoking.
      - Wear sunglasses with UV protection.
    - **Monitoring**:
      - OCT scans every 6–12 months.
      - Use Amsler grid to self-monitor vision changes.
    - **Next Steps**:
      - Discuss supplements with healthcare provider.
      - Schedule routine OCT scans to monitor progression.
'''

mh = '''**For MH (Macular Hole)**:
- **Recommendation**:
    - **Immediate Referral**: Consult retinal surgeon or specialist.
    - **Treatment Options**:
      - **Vitrectomy Surgery**: Standard treatment for full-thickness macular holes.
      - **Ocriplasmin Injection**: Non-surgical option for selected cases.
    - **Lifestyle and Monitoring**:
      - Avoid activities that increase intraocular pressure post-surgery.
      - Follow-up OCT imaging to monitor hole closure.
    - **Next Steps**:
      - Schedule surgery if indicated.
      - Regular post-operative monitoring to ensure successful recovery.
'''

normal = '''**For Normal Retina**:
- **Recommendation**: 
    - **Routine Eye Care**: Maintain regular eye exams, especially if risk factors exist.
    - **Eye Health Maintenance**:
      - Balanced diet with leafy greens, fish high in omega-3s, antioxidants.
      - Wear sunglasses with UV protection.
    - **Next Steps**:
      - Follow routine eye exams (typically every 1–2 years).
      - Maintain overall health and manage systemic conditions like diabetes or hypertension.
'''

def get_recommendation(predicted_class):
    """
    Returns recommendation text based on predicted disease class.
    """
    predicted_class = predicted_class.lower().strip()
    
    if predicted_class == "amd":
        return amd
    elif predicted_class == "cnv":
        return cnv
    elif predicted_class == "csr":
        return csr
    elif predicted_class == "dme":
        return dme
    elif predicted_class == "dr":
        return dr
    elif predicted_class == "drusen":
        return drusen
    elif predicted_class == "mh":
        return mh
    elif predicted_class == "normal":
        return normal
    else:
        return "No specific recommendation found for this condition."