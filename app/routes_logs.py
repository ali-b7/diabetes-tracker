from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import GlucoseLog, InsulinLog

logs_bp = Blueprint("logs", __name__)


@logs_bp.get("/")
def dashboard():
    glucose = (
        GlucoseLog.query
        .order_by(GlucoseLog.recorded_at.desc())
        .limit(10)
        .all()
    )
    insulin = (
        InsulinLog.query
        .order_by(InsulinLog.recorded_at.desc())
        .limit(10)
        .all()
    )
    return render_template("dashboard.html", glucose=glucose, insulin=insulin)


@logs_bp.get("/log/glucose")
def glucose_form():
    return render_template("glucose_form.html")


@logs_bp.post("/log/glucose")
def glucose_post():
    try:
        value = float(request.form.get("value", ""))
        unit = request.form.get("unit", "mg/dL")
        recorded_at_str = request.form.get("recorded_at", "")
        notes = request.form.get("notes", "").strip()

        recorded_at = (
            datetime.fromisoformat(recorded_at_str)
            if recorded_at_str
            else datetime.utcnow()
        )

        entry = GlucoseLog(
            value=value,
            unit=unit,
            recorded_at=recorded_at,
            notes=notes,
        )
        db.session.add(entry)
        db.session.commit()

        flash("Glucose entry saved.")
        return redirect(url_for("logs.dashboard"))
    except ValueError:
        flash("Please enter a valid glucose value.")
        return redirect(url_for("logs.glucose_form"))


@logs_bp.get("/log/insulin")
def insulin_form():
    return render_template("insulin_form.html")


@logs_bp.post("/log/insulin")
def insulin_post():
    try:
        insulin_type = request.form.get("insulin_type", "").strip()
        units = float(request.form.get("units", ""))
        recorded_at_str = request.form.get("recorded_at", "")
        notes = request.form.get("notes", "").strip()

        if not insulin_type:
            flash("Insulin type is required.")
            return redirect(url_for("logs.insulin_form"))

        recorded_at = (
            datetime.fromisoformat(recorded_at_str)
            if recorded_at_str
            else datetime.utcnow()
        )

        entry = InsulinLog(
            insulin_type=insulin_type,
            units=units,
            recorded_at=recorded_at,
            notes=notes,
        )
        db.session.add(entry)
        db.session.commit()

        flash("Insulin entry saved.")
        return redirect(url_for("logs.dashboard"))
    except ValueError:
        flash("Please enter valid insulin units.")
        return redirect(url_for("logs.insulin_form"))


@logs_bp.get("/history")
def history():
    glucose = (
        GlucoseLog.query
        .order_by(GlucoseLog.recorded_at.desc())
        .all()
    )
    insulin = (
        InsulinLog.query
        .order_by(InsulinLog.recorded_at.desc())
        .all()
    )
    return render_template("history.html", glucose=glucose, insulin=insulin)
