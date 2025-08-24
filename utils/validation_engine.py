"""
Validation engine for circuit analysis results to ensure accuracy and reliability.
"""
import re
from typing import Dict, List, Tuple, Any
from models.circuit_analysis import CircuitAnalysis, CircuitComponent

class CircuitValidationEngine:
    """Engine for validating circuit analysis results."""
    
    def __init__(self):
        """Initialize validation engine."""
        # Common circuit patterns and rules
        self.circuit_rules = {
            'voltage_divider': {
                'components': ['resistor', 'resistor'],
                'connections': 'series',
                'voltage_ratio': 'proportional_to_resistance'
            },
            'current_divider': {
                'components': ['resistor', 'resistor'],
                'connections': 'parallel',
                'current_ratio': 'inversely_proportional_to_resistance'
            },
            'rc_circuit': {
                'components': ['resistor', 'capacitor'],
                'time_constant': 'R * C'
            },
            'rl_circuit': {
                'components': ['resistor', 'inductor'],
                'time_constant': 'L / R'
            }
        }
        
        # Component value ranges (typical values)
        self.component_ranges = {
            'resistor': {'min': 0.1, 'max': 1000000, 'unit': 'ohm'},
            'capacitor': {'min': 0.000000001, 'max': 1, 'unit': 'farad'},
            'inductor': {'min': 0.000001, 'max': 10, 'unit': 'henry'},
            'voltage_source': {'min': 0.1, 'max': 1000000, 'unit': 'volt'},
            'current_source': {'min': 0.000001, 'max': 100, 'unit': 'ampere'}
        }
    
    def validate_analysis(self, analysis: CircuitAnalysis) -> Dict[str, Any]:
        """
        Comprehensive validation of circuit analysis results.
        
        Returns:
            Dictionary with validation results and confidence adjustments
        """
        validation_results = {
            'overall_valid': True,
            'confidence_adjustment': 0.0,
            'warnings': [],
            'errors': [],
            'suggestions': []
        }
        
        # 1. Validate circuit type consistency
        circuit_validation = self._validate_circuit_type(analysis)
        validation_results.update(circuit_validation)
        
        # 2. Validate component values
        component_validation = self._validate_component_values(analysis.components)
        validation_results.update(component_validation)
        
        # 3. Validate calculations
        calculation_validation = self._validate_calculations(analysis.calculations)
        validation_results.update(calculation_validation)
        
        # 4. Validate physical consistency
        physics_validation = self._validate_physics(analysis)
        validation_results.update(physics_validation)
        
        # 5. Calculate confidence adjustment
        validation_results['confidence_adjustment'] = self._calculate_confidence_adjustment(validation_results)
        
        return validation_results
    
    def _validate_circuit_type(self, analysis: CircuitAnalysis) -> Dict[str, Any]:
        """Validate circuit type and component consistency."""
        results = {'warnings': [], 'errors': []}
        
        circuit_type_lower = analysis.circuit_type.lower()
        
        # Check for common circuit patterns
        for pattern, rules in self.circuit_rules.items():
            if pattern in circuit_type_lower:
                # Validate component count
                expected_components = len(rules['components'])
                actual_components = len(analysis.components)
                
                if actual_components < expected_components:
                    results['warnings'].append(
                        f"Circuit identified as {pattern} but only {actual_components} components found. "
                        f"Expected at least {expected_components}."
                    )
                
                # Validate component types
                component_types = [comp.name.lower() for comp in analysis.components]
                for expected_type in rules['components']:
                    if expected_type not in component_types:
                        results['warnings'].append(
                            f"Expected {expected_type} component for {pattern} circuit"
                        )
        
        return results
    
    def _validate_component_values(self, components: List[CircuitComponent]) -> Dict[str, Any]:
        """Validate component values are within reasonable ranges."""
        results = {'warnings': [], 'errors': []}
        
        for component in components:
            comp_type = component.name.lower()
            value_str = component.value.lower()
            
            # Extract numerical value and unit
            value_info = self._extract_component_value(value_str)
            if not value_info:
                results['warnings'].append(f"Could not parse value for {component.name}: {component.value}")
                continue
            
            value, unit = value_info
            
            # Check if component type is known
            if comp_type in self.component_ranges:
                expected_range = self.component_ranges[comp_type]
                
                # Convert to base units for comparison
                normalized_value = self._normalize_value(value, unit, expected_range['unit'])
                
                if normalized_value < expected_range['min']:
                    results['warnings'].append(
                        f"{component.name} value {component.value} seems unusually low"
                    )
                elif normalized_value > expected_range['max']:
                    results['warnings'].append(
                        f"{component.name} value {component.value} seems unusually high"
                    )
        
        return results
    
    def _validate_calculations(self, calculations: List[str]) -> Dict[str, Any]:
        """Validate mathematical calculations for consistency."""
        results = {'warnings': [], 'errors': []}
        
        # Look for common calculation patterns
        for calc in calculations:
            calc_lower = calc.lower()
            
            # Check for division by zero
            if '÷0' in calc or '/0' in calc or '÷ 0' in calc or '/ 0' in calc:
                results['errors'].append(f"Division by zero detected: {calc}")
            
            # Check for impossible results
            if '= -' in calc and any(word in calc_lower for word in ['resistance', 'capacitance', 'inductance']):
                results['warnings'].append(f"Negative value for passive component: {calc}")
            
            # Check for unit consistency
            if 'ohm' in calc_lower and 'farad' in calc_lower:
                # RC time constant should be in seconds
                if 'time' in calc_lower and 'second' not in calc_lower:
                    results['warnings'].append(f"Time constant calculation should result in seconds: {calc}")
        
        return results
    
    def _validate_physics(self, analysis: CircuitAnalysis) -> Dict[str, Any]:
        """Validate physical consistency of the circuit."""
        results = {'warnings': [], 'errors': []}
        
        # Check for power conservation
        if 'power' in analysis.analysis_summary.lower():
            # Look for power calculations
            power_pattern = r'power.*=.*(\d+\.?\d*)'
            power_matches = re.findall(power_pattern, analysis.analysis_summary, re.IGNORECASE)
            
            if len(power_matches) > 1:
                # Check if power values are reasonable
                powers = [float(p) for p in power_matches]
                if max(powers) > 1000:  # More than 1kW
                    results['warnings'].append("High power values detected - verify component ratings")
        
        # Check for voltage/current relationships
        if 'voltage' in analysis.analysis_summary.lower() and 'current' in analysis.analysis_summary.lower():
            # Ohm's law validation
            voltage_pattern = r'voltage.*=.*(\d+\.?\d*)'
            current_pattern = r'current.*=.*(\d+\.?\d*)'
            resistance_pattern = r'resistance.*=.*(\d+\.?\d*)'
            
            voltages = re.findall(voltage_pattern, analysis.analysis_summary, re.IGNORECASE)
            currents = re.findall(current_pattern, analysis.analysis_summary, re.IGNORECASE)
            resistances = re.findall(resistance_pattern, analysis.analysis_summary, re.IGNORECASE)
            
            if voltages and currents and resistances:
                try:
                    v = float(voltages[0])
                    i = float(currents[0])
                    r = float(resistances[0])
                    
                    # Check if V = I * R holds approximately
                    if abs(v - (i * r)) > 0.1 * v:  # 10% tolerance
                        results['warnings'].append("Voltage/current/resistance relationship may be inconsistent")
                except ValueError:
                    pass
        
        return results
    
    def _extract_component_value(self, value_str: str) -> Tuple[float, str]:
        """Extract numerical value and unit from component value string."""
        # Common patterns: "100 ohm", "10k", "47μF", "1.5V"
        patterns = [
            r'(\d+\.?\d*)\s*([a-zA-ZΩμμ]+)',  # "100 ohm", "47μF"
            r'(\d+\.?\d*)([kmμ])',  # "10k", "47μ"
            r'(\d+\.?\d*)([VvAa])',  # "1.5V", "100mA"
        ]
        
        for pattern in patterns:
            match = re.match(pattern, value_str)
            if match:
                value = float(match.group(1))
                unit = match.group(2)
                
                # Handle multipliers
                if unit.lower() == 'k':
                    value *= 1000
                    unit = 'ohm'
                elif unit.lower() == 'm':
                    value *= 0.001
                    unit = 'ohm'
                elif unit.lower() == 'μ' or unit.lower() == 'u':
                    value *= 0.000001
                    unit = 'farad'
                
                return value, unit
        
        return None, None
    
    def _normalize_value(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert value between units for comparison."""
        # Simple conversion for common cases
        if from_unit == to_unit:
            return value
        
        # Add more conversions as needed
        # This is a simplified version
        return value
    
    def _calculate_confidence_adjustment(self, validation_results: Dict[str, Any]) -> float:
        """Calculate confidence adjustment based on validation results."""
        adjustment = 0.0
        
        # Penalize for errors
        adjustment -= len(validation_results['errors']) * 0.2
        
        # Penalize for warnings
        adjustment -= len(validation_results['warnings']) * 0.1
        
        # Bonus for passing all validations
        if not validation_results['errors'] and not validation_results['warnings']:
            adjustment += 0.1
        
        return max(-0.5, min(0.2, adjustment))  # Limit adjustment to [-0.5, 0.2]
    
    def generate_validation_report(self, validation_results: Dict[str, Any]) -> str:
        """Generate a human-readable validation report."""
        report = "## 🔍 Validation Report\n\n"
        
        if validation_results['overall_valid']:
            report += "✅ **Overall Validation: PASSED**\n\n"
        else:
            report += "❌ **Overall Validation: FAILED**\n\n"
        
        if validation_results['confidence_adjustment'] != 0:
            report += f"📊 **Confidence Adjustment:** {validation_results['confidence_adjustment']:+.2f}\n\n"
        
        if validation_results['errors']:
            report += "### ❌ Errors Found:\n"
            for error in validation_results['errors']:
                report += f"- {error}\n"
            report += "\n"
        
        if validation_results['warnings']:
            report += "### ⚠️ Warnings:\n"
            for warning in validation_results['warnings']:
                report += f"- {warning}\n"
            report += "\n"
        
        if validation_results['suggestions']:
            report += "### 💡 Suggestions:\n"
            for suggestion in validation_results['suggestions']:
                report += f"- {suggestion}\n"
            report += "\n"
        
        return report
