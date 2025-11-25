import streamlit as st
import pandas as pd
import joblib
import os


st.set_page_config(page_title="Lifestyle Pro", page_icon="💪", layout="wide")

@st.cache_resource

def load_model_assets():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models = {}
    try:
        models['burn_model'] = joblib.load(os.path.join(current_dir, "smartburn_model.pkl"))
        models['burn_cols'] = joblib.load(os.path.join(current_dir, "smartburn_columns.pkl"))

        models['diet_model'] = joblib.load(os.path.join(current_dir, "nutriFit_model.pkl"))
        models['diet_cols'] = joblib.load(os.path.join(current_dir, "model_columns.pkl"))

        models['raw_df'] = pd.read_csv(os.path.join(current_dir, "Final_data.csv"))

        return models
    except FileNotFoundError as e:
        st.error(f"🚨 HATA Dosya Bulunamadi: {e}")
        return None
    

models2 = load_model_assets()
if models2 is None:
    st.stop()

# --- 3. MAIN MENU (SIDEBAR) ---

st.sidebar.title("💪 Lifestyle Pro 💪")
menu = st.sidebar.radio("Choice mode:", ["🏠 Home page", "🔥SmartBurn AI", "🥗 NutriFit AI", "📋 FitPlan AI"])
st.sidebar.divider()
st.sidebar.info("Developed by Ihsan TAYMAS")

#  HOME PAGE

if menu == "🏠 Home page":
    st.title("💪 Lifestyle Pro 💪")
    st.markdown("""

    Welcome to **Lifestyle pro**, your all-in-one solution for fitness and nutrition!

    👈**please chose one of the model from left side menu.**
    
    * **🔥 SmartBurn:** calculates training calories.
    * **🥗 NutriFit:** tells you if your meal is healthy.
    * **📋 FitPlan:** creates a personalized workout plan based on your goals and equipment.
                
     """)
    
elif menu == "🔥SmartBurn AI":
    st.header("🔥 SmartBurn AI Module Activated!")
    st.markdown("Please proceed to the SmartBurn AI section to calculate your workout calories.")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Personal Information")
        gender = st.radio("Gender",["Male","Female"],horizontal = True)
        age = st.number_input("Age",10,90,25)
        weight = st.number_input("Weight (kg)",30.0,150.0,70.0)
        height = st.number_input("Height (m)",1.20,2.20,1.75)
    
    with col2:
        st.subheader("Workout Details")
        duration = st.slider("Workout Duration (Hours)",0.5,3.0,1.0,step=0.1)
        workout_types = ['Cardio', 'HIIT', 'Strength', 'Yoga']
        select_workout = st.selectbox("Workout Type", workout_types)
        intensity = st.select_slider(
            "Workout Intensity",
            options=["Low", "Medium", "High"]
        )

    if st.button("Calculate My Calories", type="primary", use_container_width=True):
        # 1. Nabız Tahmini
        if intensity == "Low":
            avg_bpm = 110
        elif intensity == "Medium":
            avg_bpm = 130
        else:
            avg_bpm = 150

        input_data = {
        'Age': age,
        'Weight (kg)': weight,
        'Height (m)': height,
        'Session_Duration (hours)': duration,
        'Avg_BPM': avg_bpm,
        'Fat_Percentage': 20.0, 
        'Water_Intake (liters)': 2.0, 
        'Workout_Frequency (days/week)': 3,
        'Experience_Level': 2, 
        'BMI': weight / (height**2)
    }

    
        df_input = pd.DataFrame([input_data])

       
        df_final = pd.DataFrame(columns=models2['burn_cols'])
    
        
        df_final.loc[0] = 0

    
        for col in df_input.columns:
            if col in df_final.columns:
               df_final.loc[0, col] = df_input.loc[0, col]


        target_col = f"Workout_Type_{select_workout}"
        if target_col in df_final.columns:
            df_final.loc[0, target_col] = 1

        if gender == "Male" and 'Gender_Male' in df_final.columns:
           df_final.loc[0, 'Gender_Male'] = 1

       
        prediction1 = models2['burn_model'].predict(df_final)[0]
        prediction = prediction1 / 2.5

        st.divider()
        st.success(f"🏃‍♂️ Tahmini Yakılan Kalori: **{prediction:.0f} kcal**")
        st.progress(min(int(prediction)/1000, 1.0), text="Günlük Hedef (1000 kcal)")

elif menu == "🥗 NutriFit AI":
    st.header("🥗 NutriFit AI Module Activated!")
    st.markdown("Please proceed to the NutriFit AI section to evaluate your meal's healthiness.")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        calories = st.number_input("Calories (kcal)",0,2000,500)
        protein = st.number_input("Protein (g)",0,200,20)
        carbs = st.number_input("Carbohydrates (g)",0,200,50)
    with col2:
        fats = st.number_input("Fats (g)",0,100,10)
        sugar = st.number_input("Sugar (g)",0,100,10)
        diet_types = st.selectbox("Diet Type", ["Balanced","Low Carb", "Vegan", "Keto"])

    if st.button("Evaluate My Meal", type="primary"):
        input_data = {
            'Calories': calories, 'Proteins': protein, 
            'Carbs': carbs, 'Fats': fats, 'sugar_g': sugar
        }

        df_input = pd.DataFrame([input_data])
        model_cols = models2['diet_cols']
        df_final = pd.DataFrame(columns=model_cols)
        df_final.loc[0] = 0

        for col in df_input.columns:
            if col in df_final.columns:
                df_final.loc[0, col] = df_input.loc[0, col]

        target_col = f"diet_type_{diet_types}"
        if target_col in df_final.columns: df_final.loc[0, target_col] = 1
        
        
        pred = models2['diet_model'].predict(df_final)[0]
        
        st.divider()
        if pred == 1:
            st.success("✅ **HEALTHY CHOICE!**")
            st.balloons()
            st.write("This meal appears to have an ideal balance of protein/sugar/fat.")
        else:
            st.error("⚠️ **WARNING! MAY BE UNHEALTHY.**")
            st.write("This meal may be high in sugar, high in fat, or low in protein.")
            
       
        st.subheader("Macro Distribution")
        macro_data = pd.DataFrame({
            'Macro': ['Protein', 'Carbohydrates', 'Fats', 'Sugar'],
            'Amount': [protein, carbs, fats, sugar]
        })
        st.bar_chart(macro_data.set_index('Macro'))


# 📋 MODULE 3: FITPLAN (Recommendation System)

elif menu == "📋 FitPlan AI":
    st.header("📋 FitPlan AI Pro")
    st.markdown("Create your personalized workout plan based on your goals and available equipment.")
    st.divider()
    
    df = models2['raw_df']
    
   
    c1, c2, c3 = st.columns(3)
    
    with c1:
        
        if 'Body Part' in df.columns:
            body_parts = sorted(df['Body Part'].dropna().astype(str).unique().tolist())
            selected_part = st.selectbox("💪 Target Area", body_parts)
            
    with c2:
      
        if 'Difficulty Level' in df.columns:
            levels = sorted(df['Difficulty Level'].dropna().astype(str).unique().tolist())
            selected_level = st.selectbox("📊 Level", levels, index=0) 
            
    with c3:
      
        if 'Equipment Needed' in df.columns:
            equipments = sorted(df['Equipment Needed'].dropna().astype(str).unique().tolist())
            # Default to 'Body Only' if available
            default_equip = ['Body Only'] if 'Body Only' in equipments else equipments[:1]
            selected_equip = st.multiselect("🛠️ Equipment", equipments, default=default_equip)
    
    # --- RECOMMENDATION ENGINE ---
    if st.button("📋 Create My Plan", type="primary", use_container_width=True):
        
        # 1. Basic Filtering (Area and Level)
        filtered_df = df[
            (df['Body Part'] == selected_part) & 
            (df['Difficulty Level'] == selected_level)
        ]
        
        # 2. Equipment Filtering (If equipment is selected)
        if selected_equip:
            # Get exercises that have ANY of the selected equipment
            filtered_df = filtered_df[filtered_df['Equipment Needed'].isin(selected_equip)]
        
        # 3. Sorting (From highest to lowest calories burned)
        sort_col = 'Burns Calories (per 30 min)' if 'Burns Calories (per 30 min)' in df.columns else 'Calories_Burned'
        if sort_col in filtered_df.columns:
            filtered_df = filtered_df.sort_values(by=sort_col, ascending=False)
            
        # 4. Cleaning (Remove duplicate names)
        if 'Name of Exercise' in df.columns:
            filtered_df = filtered_df.drop_duplicates(subset=['Name of Exercise'])
        
        # Get the first 5-10 exercises
        results = filtered_df.head(10)
        
        # --- SHOW RESULTS ---
        if not results.empty:
            st.success(f"**{selected_part}** area has **{len(results)}** suitable exercises!")
            
            for index, row in results.iterrows():
                name = row.get('Name of Exercise', 'Exercise')
                muscle_type = row.get('Type of Muscle', 'General')
                target_muscle = row.get('Target Muscle Group', '-')
                benefit = row.get('Benefit', 'Not specified')


                try:
                    sets_val = row.get('Sets', 3)
                    sets = int(float(sets_val))
                except:
                    sets = str(row.get('Sets', '3'))

                try:
                    reps_val = row.get('Reps', 12)
                    reps = int(float(reps_val))
                except:
                    reps = str(row.get('Reps', '12'))

                try:
                    cal_val = float(row.get(sort_col, 0))
                    cal = int(cal_val / 2.5)
                except:
                    cal = "belirsiz"
                
                # Expander for each exercise
                with st.expander(f"🏋️‍♂️ {name} ({muscle_type})"):
                    
                    # Split content into 3 columns
                    info1, info2, info3 = st.columns(3)
                    
                    with info1:
                        st.markdown(f"**🎯 Target Muscle:**\n{target_muscle}")
                        st.markdown(f"**🛠️ Equipment:**\n{row.get('Equipment Needed', '-')}")
                    
                    with info2:
                        st.markdown(f"**🔄 Program:**\n`{sets} Set` x `{reps} Reps`")
                        st.markdown(f"**🔥 Calories (30 min):**\n{cal} kcal")
                        
                    with info3:
                        st.markdown(f"**💡 Benefit:**\n{benefit}")
                        
        else:
            st.warning(f"⚠️ No exercises found matching the criteria. Please try changing the **Equipment** or **Level** selection.")
            st.info("Tip: Add more equipment in the 'Equipment' section to see more results.")