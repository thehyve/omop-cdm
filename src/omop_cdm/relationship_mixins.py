from typing import TYPE_CHECKING

from sqlalchemy import MetaData
from sqlalchemy.orm import Mapped, declared_attr, relationship

from omop_cdm.constants import VOCAB_SCHEMA

if TYPE_CHECKING:
    from omop_cdm.regular.cdm54 import Concept, ConceptSynonym


class ConceptRelationships:
    metadata: MetaData

    @declared_attr
    def descendants(cls) -> Mapped[list["Concept"]]:
        """
        Get all descendant concepts via the concept_ancestor table.

        Returned concepts are ordered by min_levels_of_separation.
        """
        return relationship(
            "Concept",
            secondary=lambda: cls.metadata.tables[f"{VOCAB_SCHEMA}.concept_ancestor"],
            primaryjoin="Concept.concept_id==ConceptAncestor.ancestor_concept_id",
            secondaryjoin="Concept.concept_id==ConceptAncestor.descendant_concept_id",
            order_by="ConceptAncestor.min_levels_of_separation, Concept.concept_name",
            viewonly=True,
        )

    @declared_attr
    def ancestors(cls) -> Mapped[list["Concept"]]:
        """
        Get all ancestor concepts via the concept_ancestor table.

        Returned concepts are ordered by min_levels_of_separation.
        """
        return relationship(
            "Concept",
            secondary=lambda: cls.metadata.tables[f"{VOCAB_SCHEMA}.concept_ancestor"],
            primaryjoin="Concept.concept_id==ConceptAncestor.descendant_concept_id",
            secondaryjoin="Concept.concept_id==ConceptAncestor.ancestor_concept_id",
            order_by="ConceptAncestor.min_levels_of_separation, Concept.concept_name",
            viewonly=True,
        )

    @declared_attr
    def children(cls) -> Mapped[list["Concept"]]:
        """
        Get child concepts via the 'Subsumes' relationship.

        This includes only the direct children of the concept, not any
        further descendants.
        """
        return relationship(
            "Concept",
            secondary=lambda: cls.metadata.tables[
                f"{VOCAB_SCHEMA}.concept_relationship"
            ],
            primaryjoin="and_(ConceptRelationship.concept_id_1==Concept.concept_id,"
            "ConceptRelationship.relationship_id=='Subsumes')",
            secondaryjoin="Concept.concept_id==ConceptRelationship.concept_id_2",
            order_by="Concept.concept_name",
            viewonly=True,
        )

    @declared_attr
    def parents(cls) -> Mapped[list["Concept"]]:
        """
        Get parent concepts via the 'Is a' relationship.

        This includes only the direct parents of the concept, not any
        further ancestors.
        """
        return relationship(
            "Concept",
            secondary=lambda: cls.metadata.tables[
                f"{VOCAB_SCHEMA}.concept_relationship"
            ],
            primaryjoin="and_(ConceptRelationship.concept_id_1==Concept.concept_id,"
            "ConceptRelationship.relationship_id=='Is a')",
            secondaryjoin="Concept.concept_id==ConceptRelationship.concept_id_2",
            order_by="Concept.concept_name",
            viewonly=True,
        )

    @declared_attr
    def maps_to(cls) -> Mapped[list["Concept"]]:
        """Get target concepts via the 'Maps to' relationship."""
        return relationship(
            "Concept",
            secondary=lambda: cls.metadata.tables[
                f"{VOCAB_SCHEMA}.concept_relationship"
            ],
            primaryjoin="and_(ConceptRelationship.concept_id_1==Concept.concept_id,"
            "ConceptRelationship.relationship_id=='Maps to')",
            secondaryjoin="Concept.concept_id==ConceptRelationship.concept_id_2",
            order_by="Concept.concept_name",
            viewonly=True,
        )

    @declared_attr
    def maps_to_value(cls) -> Mapped[list["Concept"]]:
        """Get target concepts via the 'Maps to value' relationship."""
        return relationship(
            "Concept",
            secondary=lambda: cls.metadata.tables[
                f"{VOCAB_SCHEMA}.concept_relationship"
            ],
            primaryjoin="and_(ConceptRelationship.concept_id_1==Concept.concept_id,"
            "ConceptRelationship.relationship_id=='Maps to value')",
            secondaryjoin="Concept.concept_id==ConceptRelationship.concept_id_2",
            order_by="Concept.concept_name",
            viewonly=True,
        )

    @declared_attr
    def synonyms(cls) -> Mapped[list["ConceptSynonym"]]:
        return relationship(
            primaryjoin="Concept.concept_id==ConceptSynonym.concept_id",
            back_populates="concept",
            viewonly=True,
        )
