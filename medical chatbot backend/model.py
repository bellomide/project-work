class MedicalAdviceModel:
    """Simple rule-based medical advice model"""
    
    def __init__(self):
        self.knowledge_base = {
            "malaria": {
                "symptoms": ["fever", "chills", "headache", "sweating", "fatigue", "nausea", "vomiting", "body aches"],
                "advice": [
                    "Seek immediate medical attention for proper diagnosis",
                    "Get tested with a rapid diagnostic test or blood smear",
                    "Take antimalarial medication as prescribed by a doctor",
                    "Stay hydrated and get plenty of rest",
                    "Use mosquito nets and repellents to prevent further bites",
                    "Complete the full course of medication even if you feel better"
                ],
                "prevention": [
                    "Sleep under insecticide-treated mosquito nets",
                    "Use mosquito repellent on exposed skin",
                    "Wear long-sleeved clothing in the evening",
                    "Keep windows and doors closed or screened",
                    "Eliminate standing water around your home"
                ]
            },
            "typhoid": {
                "symptoms": ["prolonged fever", "weakness", "stomach pain", "headache", "loss of appetite", "rash"],
                "advice": [
                    "Consult a doctor immediately for blood tests and diagnosis",
                    "Take prescribed antibiotics for the full duration",
                    "Drink plenty of clean, safe water to stay hydrated",
                    "Eat light, easily digestible foods",
                    "Maintain strict hygiene to prevent spreading",
                    "Get adequate rest during recovery"
                ],
                "prevention": [
                    "Drink only boiled or bottled water",
                    "Avoid raw fruits and vegetables unless you peel them yourself",
                    "Wash hands frequently with soap and water",
                    "Get vaccinated if you're in a high-risk area",
                    "Avoid street food and ice in drinks"
                ]
            },
            "nausea": {
                "symptoms": ["upset stomach", "urge to vomit", "dizziness", "sweating"],
                "advice": [
                    "Sip clear fluids like water or ginger tea slowly",
                    "Eat small amounts of bland foods (crackers, toast, rice)",
                    "Avoid strong smells and greasy or spicy foods",
                    "Rest in a comfortable position with your head elevated",
                    "Try ginger or peppermint (natural remedies)",
                    "See a doctor if nausea persists for more than 24 hours"
                ],
                "prevention": [
                    "Eat smaller, more frequent meals",
                    "Avoid trigger foods and strong odors",
                    "Stay hydrated throughout the day",
                    "Manage stress and anxiety",
                    "Get fresh air regularly"
                ]
            },
            "std": {
                "symptoms": ["unusual discharge", "pain during urination", "sores or bumps", "itching", "pelvic pain"],
                "advice": [
                    "Visit a healthcare provider or STD clinic for testing immediately",
                    "Avoid sexual contact until you've been tested and treated",
                    "Notify your sexual partner(s) so they can get tested",
                    "Take all prescribed medication as directed",
                    "Follow up with your doctor to confirm the infection is cleared",
                    "Get tested regularly if you're sexually active"
                ],
                "prevention": [
                    "Use condoms correctly every time you have sex",
                    "Limit your number of sexual partners",
                    "Get tested regularly and encourage partners to do the same",
                    "Avoid sexual activity if you or your partner has symptoms",
                    "Consider HPV and Hepatitis B vaccinations",
                    "Communicate openly with sexual partners about STD status"
                ]
            },
            "common_cold": {
                "symptoms": ["runny nose", "sore throat", "cough", "sneezing", "mild fever", "body aches"],
                "advice": [
                    "Get plenty of rest to help your body fight the infection",
                    "Drink lots of fluids (water, warm tea, soup)",
                    "Gargle with warm salt water for sore throat",
                    "Use over-the-counter pain relievers if needed",
                    "Use a humidifier to ease congestion",
                    "See a doctor if symptoms worsen or last more than 10 days"
                ],
                "prevention": [
                    "Wash your hands frequently",
                    "Avoid close contact with people who are sick",
                    "Don't touch your face, especially eyes, nose, and mouth",
                    "Disinfect frequently touched surfaces",
                    "Maintain a healthy lifestyle with good nutrition and sleep"
                ]
            },
            "diarrhea": {
                "symptoms": ["loose watery stools", "stomach cramps", "urgency", "nausea", "fever"],
                "advice": [
                    "Stay well hydrated with water or oral rehydration solution",
                    "Eat bland foods like bananas, rice, applesauce, and toast",
                    "Avoid dairy products, fatty foods, and caffeine temporarily",
                    "Rest and allow your digestive system to recover",
                    "See a doctor if diarrhea lasts more than 2 days",
                    "Seek immediate help if you see blood in stool or have high fever"
                ],
                "prevention": [
                    "Practice good hand hygiene",
                    "Drink safe, clean water",
                    "Cook food thoroughly",
                    "Store food properly",
                    "Be cautious when traveling to areas with poor sanitation"
                ]
            },
            "headache": {
                "symptoms": ["head pain", "pressure in head", "throbbing", "sensitivity to light", "neck pain"],
                "advice": [
                    "Rest in a quiet, dark room",
                    "Apply cold or warm compress to your head or neck",
                    "Stay hydrated and drink water",
                    "Take over-the-counter pain relievers as directed",
                    "Practice relaxation techniques",
                    "See a doctor if headaches are severe, frequent, or sudden"
                ],
                "prevention": [
                    "Get regular sleep on a consistent schedule",
                    "Stay hydrated throughout the day",
                    "Manage stress levels",
                    "Avoid trigger foods and caffeine",
                    "Take regular breaks from screens"
                ]
            }
        }
    
    def predict(self, user_input):
        """
        Predict the condition based on user input
        Returns: dict with condition and advice
        """
        user_input_lower = user_input.lower()
        
        # Check for direct condition mention
        for condition in self.knowledge_base.keys():
            if condition.replace("_", " ") in user_input_lower:
                return self._format_response(condition)
        
        # Symptom-based matching
        symptom_scores = {}
        for condition, data in self.knowledge_base.items():
            score = sum(1 for symptom in data["symptoms"] if symptom in user_input_lower)
            if score > 0:
                symptom_scores[condition] = score
        
        if symptom_scores:
            best_match = max(symptom_scores, key=symptom_scores.get)
            return self._format_response(best_match, symptom_scores[best_match])
        
        return {
            "success": False,
            "message": "Could not identify condition. Please describe your symptoms or mention a condition.",
            "available_conditions": list(self.knowledge_base.keys())
        }
    
    def _format_response(self, condition, confidence=None):
        """Format the response with condition information"""
        data = self.knowledge_base[condition]
        response = {
            "success": True,
            "condition": condition.replace("_", " ").title(),
            "symptoms": data["symptoms"],
            "advice": data["advice"],
            "prevention": data["prevention"],
            "disclaimer": "This is general information only. Please consult a healthcare professional for proper diagnosis and treatment."
        }
        
        if confidence:
            response["confidence"] = f"{confidence} symptom(s) matched"
        
        return response
    
    def get_all_conditions(self):
        """Get list of all available conditions"""
        return list(self.knowledge_base.keys())
    
    def get_condition_info(self, condition):
        """Get detailed information about a specific condition"""
        condition_key = condition.lower().replace(" ", "_")
        
        if condition_key in self.knowledge_base:
            return self._format_response(condition_key)
        else:
            return {
                "success": False,
                "error": "Condition not found",
                "available_conditions": self.get_all_conditions()
            }


# Example usage
if __name__ == "__main__":
    model = MedicalAdviceModel()
    
    # Test predictions
    test_cases = [
        "I have fever and chills",
        "I'm experiencing nausea and dizziness",
        "What should I do for malaria?",
        "I have a headache and sensitivity to light"
    ]
    
    print("Medical Advice Model - Test Cases\n")
    print("=" * 50)
    
    for test in test_cases:
        print(f"\nInput: {test}")
        result = model.predict(test)
        
        if result["success"]:
            print(f"Condition: {result['condition']}")
            print(f"Top 3 Advice:")
            for i, advice in enumerate(result['advice'][:3], 1):
                print(f"  {i}. {advice}")
        else:
            print(f"Message: {result['message']}")
        
        print("-" * 50)